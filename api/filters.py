import django_filters
from .models import Carro, Especie, Dinossauro

class CarroFilter(django_filters.FilterSet):
    # Filtro de preço mínimo e máximo
    preco_min = django_filters.NumberFilter(field_name="preco", lookup_expr="gte")
    preco_max = django_filters.NumberFilter(field_name="preco", lookup_expr="lte")

    # Busca por parte do nome do modelo (case-insensitive)
    modelo = django_filters.CharFilter(field_name="modelo", lookup_expr="icontains")

    class Meta:
        model = Carro
        fields = ['ano', 'marca', 'preco_min', 'preco_max', 'modelo']

class EspecieFilter(django_filters.FilterSet):
    # Faixa de periculosidade (ex: ?periculosidade_min=5&periculosidade_max=8)
    periculosidade_min = django_filters.NumberFilter(field_name="nivel_periculosidade", lookup_expr="gte")
    periculosidade_max = django_filters.NumberFilter(field_name="nivel_periculosidade", lookup_expr="lte")

    # Busca por parte do nome da espécie (case-insensitive)
    nome = django_filters.CharFilter(field_name="nome", lookup_expr="icontains")

    class Meta:
        model = Especie
        fields = ['dieta', 'nome', 'periculosidade_min', 'periculosidade_max']

class DinossauroFilter(django_filters.FilterSet):
    # Busca por parte do nome do dinossauro (case-insensitive)
    nome = django_filters.CharFilter(field_name="nome", lookup_expr="icontains")

    class Meta:
        model = Dinossauro
        fields = ['nome', 'especie', 'cercado']