from rest_framework.routers import DefaultRouter
from .views import (
    CarroViewSet,
    FuncionarioViewSet,
    EspecieViewSet,
    CercadoViewSet,
    DinossauroViewSet,
    TuristaViewSet,
)

router = DefaultRouter()

router.register(
    r"carros",
    CarroViewSet,
    basename="carro"
)

router.register(
    r"funcionarios",
    FuncionarioViewSet,
    basename="funcionario"
)

router.register(
    r"especies",
    EspecieViewSet,
    basename="especie"
)

router.register(
    r"cercados",
    CercadoViewSet,
    basename="cercado"
)

router.register(
    r"dinossauros",
    DinossauroViewSet,
    basename="dinossauro"
)

router.register(
    r"turistas",
    TuristaViewSet,
    basename="turista"
)

urlpatterns = router.urls