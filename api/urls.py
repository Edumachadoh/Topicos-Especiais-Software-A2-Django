from rest_framework.routers import DefaultRouter
from .views import MarcaViewSet, CarroViewSet

router = DefaultRouter()
router.register(
    r"marcas",
    MarcaViewSet,
    basename="marca"
)

router.register(
    r"carros",
    CarroViewSet,
    basename="carro"
)

urlpatterns = router.urls