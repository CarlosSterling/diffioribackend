from django.db import models
from django.utils.translation import gettext_lazy as _

class HeroSlide(models.Model):
    image = models.ImageField("Imagen de Fondo", upload_to="hero/", help_text="Imagen que se mostrará en el carrusel principal. Tamaño recomendado: 1920x1080px.")
    title = models.CharField("Título (Español)", max_length=200, help_text="Título principal de la diapositiva en español.")
    title_en = models.CharField("Título (Inglés)", max_length=200, blank=True, help_text="Título principal en inglés.")
    subtitle = models.TextField("Subtítulo (Español)", help_text="Texto secundario que aparece debajo del título.")
    subtitle_en = models.TextField("Subtítulo (Inglés)", blank=True, help_text="Texto secundario en inglés.")
    button_text = models.CharField("Texto del Botón (Español)", max_length=50, default="Comprar Ahora", help_text="El texto que aparecerá dentro del botón.")
    button_text_en = models.CharField("Texto del Botón (Inglés)", max_length=50, default="Buy Now", help_text="Texto del botón en inglés.")
    button_link = models.CharField("Enlace del Botón", max_length=255, default="/productos", help_text="URL o ruta a la que redirigirá el botón (ej: /productos).")
    order = models.PositiveIntegerField("Orden", default=0, help_text="Número para determinar la posición en el carrusel (menor número aparece primero).")
    is_active = models.BooleanField("¿Está Activo?", default=True, help_text="Si está marcado, esta diapositiva será visible en la página.")

    class Meta:
        verbose_name = "Slide"
        verbose_name_plural = "Slides"
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} (Orden: {self.order})"

class HomeAbout(models.Model):
    title = models.CharField("Título de la Sección (Español)", max_length=200, help_text="Título que encabeza la sección 'Sobre Nosotros'.")
    title_en = models.CharField("Título de la Sección (Inglés)", max_length=200, blank=True)
    description = models.TextField("Descripción Corta (Español)", help_text="Breve introducción que se muestra debajo del título.")
    description_en = models.TextField("Descripción Corta (Inglés)", blank=True)
    long_description = models.TextField("Descripción Larga (Español)", help_text="Contenido detallado sobre la historia o misión de la cafetería.")
    long_description_en = models.TextField("Descripción Larga (Inglés)", blank=True)
    cta_text = models.CharField("Texto de Llamado a la Acción (Español)", max_length=100, help_text="Texto del botón o enlace para saber más.")
    cta_text_en = models.CharField("Texto de Llamado a la Acción (Inglés)", max_length=100, blank=True)
    image = models.ImageField("Imagen de la Sección", upload_to="about/", blank=True, null=True, help_text="Imagen representativa para la sección.")

    class Meta:
        verbose_name = "Sobre Nosotros"
        verbose_name_plural = "Sobre Nosotros"

    def __str__(self):
        return self.title

class HomeFeature(models.Model):
    ICON_CHOICES = [
        ("Coffee", "Café"),
        ("Award", "Premio"),
        ("Leaf", "Hoja"),
        ("Truck", "Camión"),
        ("Heart", "Corazón"),
    ]
    icon = models.CharField("Icono", max_length=50, choices=ICON_CHOICES, default="Coffee", help_text="Seleccione el icono que mejor represente esta característica.")
    title = models.CharField("Título (Español)", max_length=100, help_text="Nombre corto de la característica.")
    title_en = models.CharField("Título (Inglés)", max_length=100, blank=True)
    description = models.TextField("Descripción (Español)", help_text="Explicación detallada de esta ventaja o característica.")
    description_en = models.TextField("Descripción (Inglés)", blank=True)
    order = models.PositiveIntegerField("Orden", default=0, help_text="Prioridad de aparición.")
    is_active = models.BooleanField("¿Activo?", default=True)

    class Meta:
        verbose_name = "Características"
        verbose_name_plural = "Características"
        ordering = ["order"]

    def __str__(self):
        return self.title

class HomeCTA(models.Model):
    title = models.CharField("Título del Banner (Español)", max_length=200, help_text="Título llamativo que aparece en el banner inferior.")
    title_en = models.CharField("Título del Banner (Inglés)", max_length=200, blank=True)
    subtitle = models.TextField("Subtítulo (Español)", help_text="Texto de apoyo para el banner.")
    subtitle_en = models.TextField("Subtítulo (Inglés)", blank=True)
    cta_text = models.CharField("Texto del Botón (Español)", max_length=100, help_text="Texto que invita a la acción.")
    cta_text_en = models.CharField("Texto del Botón (Inglés)", max_length=100, blank=True)
    cta_link = models.CharField("Enlace de Acción", max_length=255, default="/#footer", help_text="Destino del click en el banner.")
    background_image = models.ImageField("Imagen de Fondo", upload_to="cta/", help_text="Imagen que se mostrará detrás de los textos del banner.")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.title
