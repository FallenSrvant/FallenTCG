from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CardInventoryViewSet,
    SealedProductCategoryViewSet,
    SealedProductInventoryViewSet,
    AccessoryBrandViewSet,
    AccesoryInventoryViewSet
)

# Creamos el router automático de Django REST Framework
router = DefaultRouter()

# Endpoints de nuestro inventario
router.register(r'cards', CardInventoryViewSet, basename='card')
router.register(r'sealed-categories', SealedProductCategoryViewSet, basename='sealed-category')
router.register(r'sealed-products', SealedProductInventoryViewSet, basename='sealed-product')
router.register(r'accessory-brands', AccessoryBrandViewSet, basename='accessory-brand')
router.register(r'accessories', AccesoryInventoryViewSet, basename='accessory')

# Las URLs de la app se generan automáticamente a partir del router
urlpatterns = [
    path('', include(router.urls)),
]