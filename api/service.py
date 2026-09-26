from .models import Marca, Carro, Funcionario, Especie, Cercado, Dinossauro


class MarcaService:
    @staticmethod
    def criar(nome, pais_origem):
        return Marca.objects.create(
            nome=nome,
            pais_origem=pais_origem
        )
    @staticmethod
    def buscar_por_id(marca_id):
        return Marca.objects.get(id=marca_id)

class CarroService:
    @staticmethod
    def criar(modelo, ano, preco, marca):
        return Carro.objects.create(
            modelo=modelo,
            ano=ano,
            preco=preco,
            marca=marca
        )

class FuncionarioService:
    @staticmethod
    def criar(nome, cargo):
        return Funcionario.objects.create(
            nome=nome,
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
    def validar_dieta_compativel(especie, cercado):
        """Carnívoros não podem dividir cercado com Herbívoros/Onívoros, e vice-versa."""
        dinos_no_cercado = Dinossauro.objects.filter(cercado=cercado).select_related('especie')

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