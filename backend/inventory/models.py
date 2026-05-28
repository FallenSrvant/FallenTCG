from django.db import models

class CardInventory(models.Model):
    # Modelo para el inventario de cartas sueltas (Singles)
    class CardCondition(models.TextChoices):
        # Estándares para el estado físico de la carta
        MINT = 'M', 'Mint'                          # Impecable: Como nueva, recién salida del sobre, sin ningún detalle.
        NEAR_MINT = 'NM', 'Near Mint'               # Casi Impecable: Mínimos detalles imperceptibles a simple vista (estándar de juego).
        LIGHTLY_PLAYED = 'LP', 'Lightly Played'     # Desgaste Ligero: Jugada con poco uso, esquinas o bordes ligeramente blanqueados.
        MODERATE_PLAYED = 'MP', 'Moderately Played' # Desgaste Moderado: Raspones evidentes, pérdida de brillo o bordes desgastados.
        HEAVY_PLAYED = 'HP', 'Heavily Played'       # Muy Desgastada: Muy jugada sin micas, dobleces menores, pero legal para torneos.
        DAMAGED = 'DMG', 'Damaged'                  # Dañada: Carta rota, mojada, rayada con marcador o con dobles profundo. Valor mínimo.

    class GameType(models.TextChoices):
        # Selector de los TCG comerciales
        YUGIOH = 'YGO', 'Yu-gi-oh!'
        POKEMON = 'PKM', 'Pokémon TCG'
        DIGIMON = 'DGM', 'Digimon TCG'
        VANGUARD = 'CFG', 'Cardfight!! Vanguard'
        MAGIC = 'MTG', 'Magic The Gathering'
        RIFTBOUND = 'RB', 'Riftbound TCG (Riot)'
        
    external_card_id = models.CharField(
        # Llave universal: ID de la carta correspondiente de la API del TCG correspondiente
        max_length=100,
        help_text="ID único de la carta en la API del TCG correspondiente"
    )
    
    game_type = models.CharField(
        # Identificador del TCG para saber a que API consultar y obtener sus datos
        max_length=3,
        choices=GameType.choices,
        help_text="Selecciona el TCG al que pertenece la carta"
    )
    
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad disponible en tienda"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio de venta de la carta en MXN"
    )
    
    rarity = models.CharField(
        max_length=50,
        default='Common',
        help_text="Rareza de la carta"    
    )
    
    condition = models.CharField(
        max_length=3,
        choices=CardCondition.choices,
        default=CardCondition.MINT,
        help_text="Estado físico de la carta"
    )
    
    # Trazabilidad basica de cambios del sistema
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de registro la carta" )
    updated_at = models.DateTimeField(auto_now=True, help_text="Fecha de última actualización de la carta")
    
    class Meta:
        verbose_name = "Carta en Inventario"
        verbose_name_plural = "Cartas en Inventario"
        ordering = ['-created_at']
        unique_together = ('external_card_id', 'game_type', 'condition', 'rarity') # Evita mezclar cartas siempre y cuando las 4 condiciones no se repitan
    
    def __str__(self):
        return f"{self.get_game_type_display()} - ID: {self.external_card_id} [{self.rarity}] ({self.get_condition_display()}) - Stock: {self.stock}"
    
class SealedProductCategory(models.Model):
    # Modelo que sirve para relacionar el tipo de producto con los TCG (Categorías dinamicas)
    class GameType(models.TextChoices):
        # Selector de los TCG comerciales
        YUGIOH = 'YGO', 'Yu-gi-oh!'
        POKEMON = 'PKM', 'Pokémon TCG'
        DIGIMON = 'DGM', 'Digimon TCG'
        VANGUARD = 'CFG', 'Cardfight!! Vanguard'
        MAGIC = 'MTG', 'Magic The Gathering'
        RIFTBOUND = 'RB', 'Riftbound TCG (Riot)'
    
    game_type = models.CharField(
        max_length=3,
        choices=GameType.choices,
        help_text="Selecciona el TCG al que pertenece el producto"
    )
    
    name = models.CharField(
        max_length=100,
        help_text="Categoría de producto (ej: Booster Box, Mega Tin, Elite Trainer Box)"
    )
    
    class Meta:
        verbose_name = "Categoría de Producto Sellado"
        verbose_name_plural = "Categorías de Productos Sellados"
        unique_together = ('game_type', 'name') # No permite duplicar la misma categoría con el mismo nombre en el mismo TCG

    def __str__(self):
        return f"[{self.get_game_type_display()}] - {self.name}"

class SealedProductInventory(models.Model):
    # Modelo para el inventario de productos sellados. Se conecta al modelo de SealedProductCategory mediante llave foranea.
    name = models.CharField(
        max_length=360,
        help_text="Nombre del producto (ej: Justice Hunters, Phantasmal flames)"
    )
    
    category = models.ForeignKey(
        # Conecta el producto con su categoria 
        SealedProductCategory,
        on_delete=models.PROTECT,
        help_text="Categoría del producto",
        related_name='products'
    )
    
    upc_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Código de barras del producto"
    )
    
    external_product_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="ID del producto en APIs de distribuidores o catálogos externos"
    )
    
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad disponible en tienda"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio de venta en MXN"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto Sellado"
        verbose_name_plural = "Productos Sellados"
        # Candado SQL: Evita duplicar exactamente el mismo producto bajo la misma categoría
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name} ({self.category.name}) - Stock: {self.stock}"

class AccessoryBrand(models.Model):
    # Modelo de catálogo dinámico de marcas de accesorios.
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre de la marca"
    )
    
    class Meta:
        verbose_name = "Marca de Accesorio"
        verbose_name_plural = "Marcas de Accesorios"

    def __str__(self):
        return self.name
    
class AccesoryInventory(models.Model):
    # Modelo para los accesorios y se conecta al modelo de las marcas de accesorio.
    class AccessoryType(models.TextChoices):
        # Tipo de accesorio
        SLEEVES = 'SLV', 'Micas / Fundas'
        DECK_BOX = 'DBX', 'Porta decks'
        PLAYMAT = 'MAT', 'Playmats'
        BINDER = 'BND', 'Carpetas / Album'
        DICE_COUNTERS = 'DIC', 'Dados / Contadores'
        PROTECTORS = 'PRT', 'Protectores rígidos (Toploaders/One-Touch)'
        COINS = 'CNS', 'Monedas / Fichas'
        
    class SizeType(models.TextChoices):
        # Tamaño del accesorio
        STANDARD = 'STD', 'Standard Size (Pokémon, Magic, Lorcana)'
        JAPANESE = 'JPN', 'Japanese / Small Size (Yu-Gi-Oh!, Vanguard)'
        UNIVERSAL = 'UNI', 'Universal / No Aplica'

    name = models.CharField(
        max_length=200, 
        help_text="Nombre descriptivo (ej: Matte Black Sleeves - 100 ct)"
    )
    
    # RELACIÓN DINÁMICA: Adiós al text choices rígido, hola al CRUD de marcas
    brand = models.ForeignKey(
        #Relación a la clase de marcas de accesorios
        AccessoryBrand,
        on_delete=models.PROTECT,
        help_text="Selecciona la marca del accesorio",
        related_name="accessories"
    )
    
    accessory_type = models.CharField(
        # Tipo de accesorio
        max_length=3,
        choices=AccessoryType.choices,
        help_text="Tipo de accesorio de juego"
    )
    
    size = models.CharField(
        # Tamaño del accesorio
        max_length=3,
        choices=SizeType.choices,
        default=SizeType.UNIVERSAL,
        help_text="Tamaño físico del accesorio"
    )
    
    color_design = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Color o arte impreso"
    )
    
    upc_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Código de barras de fábrica"
    )
    
    stock = models.PositiveIntegerField(
        default=0
    )
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Precio de venta en MXN"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Accesorio"
        verbose_name_plural = "Accesorios"
        unique_together = ('name', 'brand', 'accessory_type', 'size')  # El candado compuesto evalúa la relación de la Llave Foránea de la marca

    def __str__(self):
        return f"[{self.brand.name}] {self.name} - Stock: {self.stock}"