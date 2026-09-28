from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from api.models import Carro, Funcionario, Especie, Cercado, Dinossauro, Turista
from api.serializers import (
    CarroSerializer,
    FuncionarioSerializer,
    EspecieSerializer,
    CercadoSerializer,
    DinossauroSerializer,
    TuristaSerializer,
)
from api.filters import CarroFilter, EspecieFilter, DinossauroFilter, TuristaFilter
from api.service import (
    CarroService,
    FuncionarioService,
    EspecieService,
    CercadoService,
    DinossauroService,
    TuristaService,
)


class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.select_related("funcionario").all()
    serializer_class = CarroSerializer

    # Habilita o backend de filtros nesta view
    filter_backends = [DjangoFilterBackend]

    # Filtros por tipo/funcionario (igualdade) e nome do modelo (icontains)
    filterset_class = CarroFilter

    def perform_create(self, serializer):
        serializer.instance = CarroService.criar(**serializer.validated_data)

    def perform_update(self, serializer):
        instance = serializer.instance
        dados = serializer.validated_data

        modelo = dados.get('modelo', instance.modelo)
        tipo = dados.get('tipo', instance.tipo)
        funcionario = dados.get('funcionario', instance.funcionario)

        try:
            CarroService.atualizar(instance, modelo, tipo, funcionario)
        except ValueError as e:
            raise ValidationError(str(e))


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

    def perform_create(self, serializer):
        serializer.instance = FuncionarioService.criar(**serializer.validated_data)


class EspecieViewSet(viewsets.ModelViewSet):
    queryset = Especie.objects.all()
    serializer_class = EspecieSerializer

    # Habilita filtros por dieta (igualdade), nome (icontains) e faixa de periculosidade
    filter_backends = [DjangoFilterBackend]
    filterset_class = EspecieFilter

    def perform_create(self, serializer):
        serializer.instance = EspecieService.criar(**serializer.validated_data)

    def perform_update(self, serializer):
        instance = serializer.instance
        dados = serializer.validated_data

        nome = dados.get('nome', instance.nome)
        dieta = dados.get('dieta', instance.dieta)
        nivel_periculosidade = dados.get('nivel_periculosidade', instance.nivel_periculosidade)

        try:
            EspecieService.atualizar(instance, nome, dieta, nivel_periculosidade)
        except ValueError as e:
            raise ValidationError(str(e))


class CercadoViewSet(viewsets.ModelViewSet):
    # select_related evita consultas extras ao banco ao serializar o funcionario aninhado
    queryset = Cercado.objects.select_related("funcionario").all()
    serializer_class = CercadoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['funcionario']

    def perform_create(self, serializer):
        serializer.instance = CercadoService.criar(**serializer.validated_data)


class DinossauroViewSet(viewsets.ModelViewSet):
    queryset = Dinossauro.objects.select_related("especie", "cercado").all()
    serializer_class = DinossauroSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = DinossauroFilter

    def perform_create(self, serializer):
        try:
            serializer.instance = DinossauroService.criar(**serializer.validated_data)
        except ValueError as e:
            raise ValidationError(str(e))

    def perform_update(self, serializer):
        instance = serializer.instance
        dados = serializer.validated_data

        # PATCH manda só os campos alterados; usa o valor atual da instância
        # para os que não vieram na requisição.
        nome = dados.get('nome', instance.nome)
        data_nascimento = dados.get('data_nascimento', instance.data_nascimento)
        especie = dados.get('especie', instance.especie)
        cercado = dados.get('cercado', instance.cercado)

        try:
            DinossauroService.atualizar(instance, nome, data_nascimento, especie, cercado)
        except ValueError as e:
            raise ValidationError(str(e))


class TuristaViewSet(viewsets.ModelViewSet):
    queryset = Turista.objects.select_related("carro").all()
    serializer_class = TuristaSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = TuristaFilter

    def perform_create(self, serializer):
        try:
            serializer.instance = TuristaService.criar(**serializer.validated_data)
        except ValueError as e:
            raise ValidationError(str(e))

    def perform_update(self, serializer):
        instance = serializer.instance
        dados = serializer.validated_data

        nome = dados.get('nome', instance.nome)
        data_nascimento = dados.get('data_nascimento', instance.data_nascimento)
        carro = dados.get('carro', instance.carro)

        try:
            TuristaService.atualizar(instance, nome, data_nascimento, carro)
        except ValueError as e:
            raise ValidationError(str(e))