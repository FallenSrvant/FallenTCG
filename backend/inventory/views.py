from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import CardInventory, SealedProductCategory, SealedProductInventory, AccessoryBrand, AccesoryInventory
from .serializers import (
    CardInventorySerializer,
    SealedProductCategorySerializer,
    SealedProductInventorySerializer,
    AccessoryBrandSerializer,
    AccesoryInventorySerializer
)
class CardInventoryViewSet(viewsets.ModelViewSet):
   # Vista para las cartas sueltas
    queryset = CardInventory.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['external_card_id', 'game_type', 'condition', 'rarity']
    search_fields = ['external_card_id']
    ordering_fields = ['price', 'stock', 'created_at']
    serializer_class = CardInventorySerializer

class SealedProductCategoryViewSet(viewsets.ModelViewSet):
    # Vista para las categorías de productos sellados
    queryset = SealedProductCategory.objects.all().order_by('name')
    serializer_class = SealedProductCategorySerializer

class SealedProductInventoryViewSet(viewsets.ModelViewSet):
    # Vista para el inventario de productos sellados
    queryset = SealedProductInventory.objects.all().order_by('-created_at')
    serializer_class = SealedProductInventorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'category__name']
    ordering_fields = ['price', 'stock', 'created_at']

class AccessoryBrandViewSet(viewsets.ModelViewSet):
    # Vista para las marcas de accesorios
    queryset = AccessoryBrand.objects.all().order_by('name')
    serializer_class = AccessoryBrandSerializer

class AccesoryInventoryViewSet(viewsets.ModelViewSet):
    # Vista para el inventario de accesorios
    queryset = AccesoryInventory.objects.all().order_by('-created_at')
    serializer_class = AccesoryInventorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'brand__name', 'color']
    ordering_fields = ['price', 'stock', 'created_at']