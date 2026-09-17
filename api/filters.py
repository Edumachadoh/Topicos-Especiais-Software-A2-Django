import django_filters
from .models import Carro

class CarroFilter(django_filters.FilterSet):
    # Filtro de preço mínimo e máximo
    preco_min = django_filters.NumberFilter(field_name="preco", lookup_expr="gte")
    preco_max = django_filters.NumberFilter(field_name="preco", lookup_expr="lte")
    
    # Busca por parte do nome do modelo (case-insensitive)
    modelo = django_filters.CharFilter(field_name="modelo", lookup_expr="icontains")

    class Meta:
        model = Carro
        fields = ['ano', 'marca', 'preco_min', 'preco_max', 'modelo']