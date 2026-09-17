from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.models import Carro, Marca
from api.serializers import CarroSerializer, MarcaSerializer

class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.select_related("marca").all()
    serializer_class = CarroSerializer
    
    # Habilita o backend de filtros nesta view
    filter_backends = [DjangoFilterBackend]
    
    # Define quais campos do modelo Carro aceitarão filtro na URL
    filterset_fields = ['ano', 'marca']
    
class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer