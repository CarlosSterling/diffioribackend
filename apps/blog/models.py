from django.db import models
from django.utils.text import slugify

class BlogPost(models.Model):
    title        = models.CharField("Título del Artículo (Español)", max_length=160, help_text="Encabezado principal del artículo del blog.")
    title_en     = models.CharField("Título (Inglés)", max_length=160, blank=True)
    slug         = models.SlugField("URL Amigable", unique=True, blank=True, help_text="Identificador único para la URL del artículo.")
    cover_image  = models.ImageField("Imagen de Portada", upload_to="blog/covers/", help_text="Imagen principal que aparecerá en el listado del blog.")
    excerpt      = models.CharField("Resumen/Extracto (Español)", max_length=250, blank=True, help_text="Breve descripción que aparece en el listado antes de leer el artículo completo.")
    excerpt_en   = models.CharField("Resumen/Extracto (Inglés)", max_length=250, blank=True)
    content      = models.TextField("Contenido Completo (Español)", help_text="Cuerpo principal del artículo.")
    content_en   = models.TextField("Contenido Completo (Inglés)", blank=True)
    published_at = models.DateTimeField("Fecha de Publicación", null=True, blank=True, help_text="Fecha en la que el artículo será visible.")
    is_published = models.BooleanField("Artículo Publicado", default=False, help_text="Si está marcado, el artículo será visible para todos en la web.")

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Blog"
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:60]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
