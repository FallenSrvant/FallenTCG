from rest_framework import serializers
from .models import CardInventory, SealedProductCategory, SealedProductInventory, AccessoryBrand, AccesoryInventory


class CardInventorySerializer(serializers.ModelSerializer):
    # Cartas sueltas
    class Meta:
        model = CardInventory
        fields = '__all__'  # Convierte automáticamente todos los campos del modelo a JSON

class SealedProductCategorySerializer(serializers.ModelSerializer):
    # Categorías de productos sellados
    class Meta:
        model = SealedProductCategory
        fields = '__all__'

class SealedProductInventorySerializer(serializers.ModelSerializer):
    # Inyecta el objeto completo de la categoría en las peticiones GET (lectura)
    category_detail = SealedProductCategorySerializer(source='category', read_only=True)

    class Meta:
        model = SealedProductInventory
        fields = [
            'id', 'name', 'category', 'category_detail', 'stock', 
            'price', 'upc_code', 'external_product_id', 'created_at', 'updated_at'
        ]
        
class AccessoryBrandSerializer(serializers.ModelSerializer):
    # Marca de accesorios
    class Meta:
        model = AccessoryBrand
        fields = '__all__'

class AccesoryInventorySerializer(serializers.ModelSerializer):
    # Anidamos la marca para que el Front reciba los detalles completos (ej: {id: 1, name: "Ultra Pro"})
    brand_detail = AccessoryBrandSerializer(source='brand', read_only=True)

    class Meta:
        model = AccesoryInventory
        fields = [
            'id', 'name', 'brand', 'brand_detail', 'accessory_type', 
            'size', 'color_design', 'stock', 'price', 'upc_code', 'created_at', 'updated_at'
        ]