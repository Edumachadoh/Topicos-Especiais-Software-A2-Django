from .models import Carro, Funcionario, Especie, Cercado, Dinossauro


class CarroService:
    @staticmethod
    def criar(modelo, tipo, funcionario):
        return Carro.objects.create(
            modelo=modelo,
            tipo=tipo,
            funcionario=funcionario
        )

class FuncionarioService:
    @staticmethod
    def criar(nome, data_nascimento, cargo):
        return Funcionario.objects.create(
            nome=nome,
            data_nascimento=data_nascimento,
            cargo=cargo
        )

class EspecieService:
    @staticmethod
    def validar_mudanca_dieta(instance, nova_dieta):
        """Não deixa mudar a dieta se isso gerar conflito em algum cercado onde já há dinossauros dessa espécie."""
        if nova_dieta == instance.dieta:
            return

        cercados_com_essa_especie = Cercado.objects.filter(
            dinossauros__especie=instance
        ).distinct()

        for cercado in cercados_com_essa_especie:
            outros_dinos = Dinossauro.objects.filter(cercado=cercado) \
                .exclude(especie=instance) \
                .select_related('especie')

            for dino in outros_dinos:
                eh_carnivoro_novo = nova_dieta == 'C'
                eh_carnivoro_existente = dino.especie.dieta == 'C'

                if eh_carnivoro_novo != eh_carnivoro_existente:
                    raise ValueError(
                        f"Não é possível mudar a dieta de '{instance.nome}' para "
                        f"'{dict(Especie.DIETA_CHOICES)[nova_dieta]}', pois no cercado "
                        f"'{cercado.nome}' já existe o dinossauro '{dino.nome}', de dieta "
                        f"incompatível ('{dino.especie.get_dieta_display()}')."
                    )

    @staticmethod
    def criar(nome, dieta, nivel_periculosidade):
        return Especie.objects.create(
            nome=nome,
            dieta=dieta,
            nivel_periculosidade=nivel_periculosidade
        )

    @staticmethod
    def atualizar(instance, nome, dieta, nivel_periculosidade):
        EspecieService.validar_mudanca_dieta(instance, dieta)

        instance.nome = nome
        instance.dieta = dieta
        instance.nivel_periculosidade = nivel_periculosidade
        instance.save()
        return instance

class CercadoService:
    @staticmethod
    def criar(nome, voltagem_cerca, dimensao_m2, funcionario):
        return Cercado.objects.create(
            nome=nome,
            voltagem_cerca=voltagem_cerca,
            dimensao_m2=dimensao_m2,
            funcionario=funcionario
        )

class DinossauroService:
    @staticmethod
    def validar_dieta_compativel(especie, cercado, ignorar_dinossauro_id=None):
        """Carnívoros não podem dividir cercado com Herbívoros/Onívoros, e vice-versa."""
        dinos_no_cercado = Dinossauro.objects.filter(cercado=cercado).select_related('especie')

        if ignorar_dinossauro_id is not None:
            # Tirar o ID do dinossauro que já está no cercado da lista de verificação
            dinos_no_cercado = dinos_no_cercado.exclude(id=ignorar_dinossauro_id)

        for dino in dinos_no_cercado:
            dieta_existente = dino.especie.dieta
            eh_carnivoro_novo = especie.dieta == 'C'
            eh_carnivoro_existente = dieta_existente == 'C'

            if eh_carnivoro_novo != eh_carnivoro_existente:
                raise ValueError(
                    f"Não é possível colocar um dinossauro de dieta '{especie.get_dieta_display()}' "
                    f"no cercado '{cercado.nome}', pois já existe lá o dinossauro "
                    f"'{dino.nome}', de dieta '{dino.especie.get_dieta_display()}'."
                )

    @staticmethod
    def criar(nome, data_nascimento, especie, cercado):
        DinossauroService.validar_dieta_compativel(especie, cercado)

        return Dinossauro.objects.create(
            nome=nome,
            data_nascimento=data_nascimento,
            especie=especie,
            cercado=cercado
        )

    @staticmethod
    def atualizar(instance, nome, data_nascimento, especie, cercado):
        DinossauroService.validar_dieta_compativel(
            especie=especie,
            cercado=cercado,
            ignorar_dinossauro_id=instance.id
        )

        instance.nome = nome
        instance.data_nascimento = data_nascimento
        instance.especie = especie
        instance.cercado = cercado
        instance.save()
        return instance