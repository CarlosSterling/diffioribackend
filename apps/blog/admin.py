from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("get_thumbnail", "title", "is_published", "published_at", "edit_button")
    list_display_links = ("get_thumbnail", "title", "edit_button")
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "excerpt", "content")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    actions = ["make_published", "make_unpublished", "duplicate_post"]
    exclude = ("title_en", "excerpt_en", "content_en")
    save_on_top = True

    def edit_button(self, obj):
        if obj.pk:
            url = reverse('admin:blog_blogpost_change', args=[obj.pk])
            return format_html(
                '<a href="{}" class="edit-icon-link" title="Editar elemento">'
                '<i class="fas fa-pencil-alt"></i></a>',
                url
            )
        return "-"
    edit_button.short_description = "Acciones"
    fieldsets = (
        ("Contenido Principal", {
            "fields": ("title", "slug", ("cover_image", "cover_preview"), "excerpt", "content")
        }),
        ("Publicación", {
            "fields": ("is_published", "published_at")
        }),
    )
    readonly_fields = ("cover_preview",)

    def get_thumbnail(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width: 60px; height: 35px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />', obj.cover_image.url)
        return format_html('<div style="width: 60px; height: 35px; background: #eee; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #999;">N/A</div>')
    get_thumbnail.short_description = "Imagen del Artículo"

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width: 200px; height: auto; border-radius: 8px; border: 1px solid #ddd;" />', obj.cover_image.url)
        return "No hay imagen cargada"
    cover_preview.short_description = "Vista Previa de la Portada"



    @admin.action(description="Publicar posts seleccionados")
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} posts publicados con éxito.")

    @admin.action(description="Ocultar posts seleccionados")
    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} posts ocultados con éxito.")

    @admin.action(description="Duplicar artículos seleccionados")
    def duplicate_post(self, request, queryset):
        for post in queryset:
            post.pk = None
            post.title = f"{post.title} (Copia)"
            post.slug = ""
            post.is_published = False
            post.save()
        self.message_user(request, f"{queryset.count()} artículos duplicados como borradores.")
