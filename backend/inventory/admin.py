from django.contrib import admin
from .models import CardInventory, SealedProductCategory, SealedProductInventory, AccessoryBrand, AccesoryInventory

@admin.register(CardInventory)
class CardInventoryAdmin(admin.ModelAdmin):
    # Columnas que se veran en la lista principal del panel de administración
    list_display = ('external_card_id', 'game_type', 'stock', 'price', 'rarity', 'condition', 'created_at', 'updated_at')
    
    # Filtros laterales para busqueda rápida del inventario
    list_filter = ('game_type', 'rarity', 'condition')
    
    # Buscador por ID externo (para buscar una carta especifica)
    search_fields = ('external_card_id',)
    
    # Permite editar el precio y el stock directamente desde la lista sin entrar a la carta
    list_editable = ('price', 'stock')
    
    # Paginación para que no sature la pantalla
    list_per_page = 20
    
@admin.register(SealedProductCategory)
class SealedProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('game_type', 'name')
    list_filter = ('game_type',)
    search_fields = ('name',)
    list_per_page = 20

@admin.register(SealedProductInventory)
class SealedProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock', 'price', 'upc_code')
    list_filter = ('category__game_type','category') #Filtra usando la relación de la foreign key
    search_fields = ('name','upc_code','external_product_id')
    list_editable = ('stock', 'price')
    list_per_page = 20
    
@admin.register(AccessoryBrand)
class AccessoryBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20

@admin.register(AccesoryInventory)
class AccesoryInventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'accessory_type', 'size', 'stock', 'price')
    list_filter = ('brand', 'accessory_type', 'size')
    search_fields = ('name', 'color_design', 'upc_code')
    list_editable = ('stock', 'price')
    list_per_page = 20