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

    # Habilita filtro simples por dieta (ex: /api/especies/?dieta=C)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dieta']


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
    filterset_fields = ['especie', 'cercado']