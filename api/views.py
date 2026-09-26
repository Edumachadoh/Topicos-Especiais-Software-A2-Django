from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.models import Carro, Marca, Funcionario, Especie, Cercado, Dinossauro
from api.serializers import (
    CarroSerializer,
    MarcaSerializer,
    FuncionarioSerializer,
    EspecieSerializer,
    CercadoSerializer,
    DinossauroSerializer,
)
from api.filters import EspecieFilter, DinossauroFilter


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


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer


class EspecieViewSet(viewsets.ModelViewSet):
    queryset = Especie.objects.all()
    serializer_class = EspecieSerializer

    # Habilita filtros por dieta (igualdade), nome (icontains) e faixa de periculosidade
    filter_backends = [DjangoFilterBackend]
    filterset_class = EspecieFilter


class CercadoViewSet(viewsets.ModelViewSet):
    # select_related evita consultas extras ao banco ao serializar o funcionario aninhado
    queryset = Cercado.objects.select_related("funcionario").all()
    serializer_class = CercadoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['funcionario']


class DinossauroViewSet(viewsets.ModelViewSet):
    queryset = Dinossauro.objects.select_related("especie", "cercado").all()
    serializer_class = DinossauroSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = DinossauroFilter