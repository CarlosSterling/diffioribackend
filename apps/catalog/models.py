from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name    = models.CharField("Nombre de la Categoría", max_length=60, help_text="Ej: Cafés, Repostería, etc.")
    name_en = models.CharField("Nombre (Inglés)", max_length=60, blank=True)
    slug    = models.SlugField("URL Amigable", unique=True, blank=True, help_text="Identificador único para la URL. Se genera automáticamente si se deja vacío.")
    order   = models.PositiveIntegerField("Orden de Visualización", default=0)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:60]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    # ───── Datos principales ─────
    name        = models.CharField("Nombre del Producto", max_length=120)
    name_en     = models.CharField("Nombre (Inglés)", max_length=120, blank=True)
    slug        = models.SlugField("URL Amigable", unique=True, blank=True, help_text="Identificador único para la URL del producto.")
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Categoría"
    )

    cover = models.ImageField(
        "Imagen de Portada",
        upload_to="products/cover/",
        blank=True,
        null=True,
        help_text="Imagen principal que aparecerá en el catálogo."
    )

    short_desc     = models.CharField("Descripción Corta", max_length=160, blank=True, help_text="Pequeña frase descriptiva para listados. Se autogenera de la descripción si se deja vacía.")
    short_desc_en  = models.CharField("Descripción Corta (Inglés)", max_length=160, blank=True)
    description    = models.TextField("Descripción Completa")
    description_en = models.TextField("Descripción Completa (Inglés)", blank=True)

    price       = models.DecimalField("Precio Base", max_digits=12, decimal_places=2, help_text="Precio de venta base o para la variante principal.", null=True, blank=True)
    stock       = models.PositiveIntegerField("Stock / Cantidad", default=0, help_text="Cantidad de unidades disponibles.")
    data_sheet  = models.FileField(                # PDF o ficha técnica
        "Ficha Técnica (PDF)",
        upload_to="products/datasheets/",
        blank=True,
        help_text="Archivo descargable opcional con especificaciones técnicas."
    )

    # ───── Control ─────
    is_active   = models.BooleanField("Producto Disponible", default=True, help_text="Se desactiva automáticamente si el stock es 0.")
    created_at  = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def save(self, *args, **kwargs):
        # autogenera slug la primera vez
        if not self.slug:
            self.slug = slugify(self.name)[:60]
        
        # autogenera short_desc si está vacío
        if not self.short_desc and self.description:
            # Limpia espacios y toma los primeros 155 caracteres con puntos suspensivos
            desc = self.description.strip()
            if len(desc) > 155:
                self.short_desc = desc[:152] + "..."
            else:
                self.short_desc = desc
        
        # Lógica de Stock: Si es 0 o menor, se desactiva automáticamente
        if self.stock <= 0:
            self.is_active = False
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    Imágenes adicionales (galería) asociadas a cada producto.
    """
    product = models.ForeignKey(
        Product,
        related_name="gallery",
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    image   = models.ImageField("Imagen", upload_to="products/gallery/", help_text="Cargue fotos adicionales para mostrar en la galería del producto.")
    alt     = models.CharField("Texto Alternativo (Accesibilidad)", max_length=120, blank=True, help_text="Breve descripción de la imagen para personas con discapacidad visual.")

    class Meta:
        verbose_name = "imagen"
        verbose_name_plural = "Galería"

    def __str__(self):
        return f"{self.product.name} – #{self.id}"


class ProductVariant(models.Model):
    """
    Opciones específicas para productos (ej: gramaje y molienda de café).
    """
    product = models.ForeignKey(
        Product,
        related_name="variants",
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    
    weight = models.CharField("Peso/Gramaje", max_length=50, help_text="Ej: 250 gr, 500 gr")
    grind  = models.CharField("Molienda/Presentación", max_length=100, help_text="Ej: Molido, En pepa, Cápsulas")
    
    price  = models.DecimalField("Precio de esta Variante", max_digits=12, decimal_places=2)
    stock  = models.PositiveIntegerField("Stock", default=0)
    
    is_active = models.BooleanField("Habilitada", default=True)

    class Meta:
        verbose_name = "Variante de Producto"
        verbose_name_plural = "Variantes de Producto"
        ordering = ["price"]

    def __str__(self):
        return f"{self.product.name} - {self.weight} ({self.grind})"
