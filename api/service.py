from .models import Marca, Carro, Funcionario


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