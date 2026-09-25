from rest_framework import serializers
from .models import Marca, Carro


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = [
            "id",
            "nome",
            "pais_origem",
        ]


class CarroSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer(read_only=True)
    marca_id = serializers.PrimaryKeyRelatedField(
        source="marca",
        queryset=Marca.objects.all(),
        write_only=True
    )

    class Meta:
        model = Carro
        fields = [
            "id",
            "modelo",
            "ano",
            "preco",
            "marca",
            "marca_id",
        ]


# serializer de dinossauros (NOVOS)
from .models import Especie, Cercado, Dinossauro, Funcionario


class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = ['id', 'nome', 'dieta', 'nivel_periculosidade']


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'nome', 'cargo']


class CercadoSerializer(serializers.ModelSerializer):
    # Leitura: Traz os dados do funcionário ao buscar um cercado
    funcionario = FuncionarioSerializer(read_only=True)

    # Escrita: Recebe apenas o ID do funcionário ao criar/atualizar um cercado
    funcionario_id = serializers.PrimaryKeyRelatedField(
        source='funcionario',
        queryset=Funcionario.objects.all(),
        write_only=True
    )

    class Meta:
        model = Cercado
        fields = [
            'id',
            'nome',
            'voltagem_cerca',
            'dimensao_m2',
            'funcionario',
            'funcionario_id'
        ]


class DinossauroSerializer(serializers.ModelSerializer):
    # Campos aninhados para LEITURA (traz o objeto completo no GET)
    especie = EspecieSerializer(read_only=True)
    cercado = CercadoSerializer(read_only=True)

    # Campos de ID para ESCRITA (recebe apenas o número no POST/PUT)
    especie_id = serializers.PrimaryKeyRelatedField(
        source='especie',
        queryset=Especie.objects.all(),
        write_only=True
    )
    cercado_id = serializers.PrimaryKeyRelatedField(
        source='cercado',
        queryset=Cercado.objects.all(),
        write_only=True
    )

    class Meta:
        model = Dinossauro
        fields = [
            'id',
            'nome',
            'data_nascimento',
            'especie',
            'especie_id',
            'cercado',
            'cercado_id'
        ]