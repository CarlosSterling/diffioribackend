# apps/clients/models.py
from django.db import models
from django.utils.text import slugify

class Client(models.Model):
    name        = models.CharField("Nombre del Cliente/Empresa", max_length=120)
    slug        = models.SlugField("URL Amigable", unique=True, blank=True, help_text="Se genera automáticamente. Identificador único para la URL.")
    logo        = models.ImageField("Logo", upload_to="clients/logos/", blank=True, help_text="Logo del cliente o empresa.")
    cover = models.ImageField(
        "Imagen de Portada",
        upload_to="clients/covers/",
        blank=True,
        null=True,
        help_text="Imagen opcional para destacar este cliente."
    )
    testimonial = models.TextField("Testimonio (Español)", help_text="Comentario o reseña del cliente sobre la cafetería.")
    testimonial_en = models.TextField("Testimonio (Inglés)", blank=True)
    location    = models.CharField("Ubicación/Ciudad", max_length=120, blank=True, help_text="Ciudad o zona del cliente.")
    latitude    = models.DecimalField("Latitud", max_digits=18, decimal_places=15, null=True, blank=True, help_text="Coordenada de latitud para el mapa.")
    longitude   = models.DecimalField("Longitud", max_digits=18, decimal_places=15, null=True, blank=True, help_text="Coordenada de longitud para el mapa.")
    is_active   = models.BooleanField("Cliente Visible", default=True, help_text="Si está marcado, este cliente aparecerá en la web.")
    created_at  = models.DateTimeField("Fecha de Registro", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:60]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ClientImage(models.Model):
    client = models.ForeignKey(Client, related_name="gallery", on_delete=models.CASCADE, verbose_name="Cliente")
    image  = models.ImageField("Imagen", upload_to="clients/gallery/", help_text="Foto adicional del cliente o sus proyectos.")
    alt    = models.CharField("Texto Alternativo", max_length=120, blank=True)

    class Meta:
        verbose_name = "imagen"
        verbose_name_plural = "Galería"

    def __str__(self):
        return f"{self.client.name} – {self.id}"
