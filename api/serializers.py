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