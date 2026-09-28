from datetime import date

from .models import Carro, Funcionario, Especie, Cercado, Dinossauro, Turista


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
    def criar(nome, dieta, nivel_periculosidade):
        return Especie.objects.create(
            nome=nome,
            dieta=dieta,
            nivel_periculosidade=nivel_periculosidade
        )

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

class TuristaService:
    IDADE_MINIMA_PARA_CARRO = 18

    @staticmethod
    def calcular_idade(data_nascimento):
        hoje = date.today()
        return hoje.year - data_nascimento.year - (
            (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
        )

    @staticmethod
    def validar_carro(data_nascimento, carro):
        """Só carros de Turismo podem ser usados, e só por maiores de idade."""
        if carro is None:
            return

        if carro.tipo != 'T':
            raise ValueError(
                f"O carro '{carro.modelo}' é do tipo '{carro.get_tipo_display()}', "
                f"não de Turismo — não pode ser atribuído a um turista."
            )

        idade = TuristaService.calcular_idade(data_nascimento)
        if idade < TuristaService.IDADE_MINIMA_PARA_CARRO:
            raise ValueError(
                f"Turista de {idade} anos é menor de idade e não pode ser vinculado "
                f"a um carro (mínimo {TuristaService.IDADE_MINIMA_PARA_CARRO} anos)."
            )

    @staticmethod
    def criar(nome, data_nascimento, carro=None):
        TuristaService.validar_carro(data_nascimento, carro)

        return Turista.objects.create(
            nome=nome,
            data_nascimento=data_nascimento,
            carro=carro
        )

    @staticmethod
    def atualizar(instance, nome, data_nascimento, carro=None):
        TuristaService.validar_carro(data_nascimento, carro)

        instance.nome = nome
        instance.data_nascimento = data_nascimento
        instance.carro = carro
        instance.save()
        return instance