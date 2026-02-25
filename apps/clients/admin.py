from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Client, ClientImage


class ClientImageInline(admin.TabularInline):
    model = ClientImage
    extra = 1
    fields = ("image", "thumbnail", "alt")
    readonly_fields = ("thumbnail",)

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 8px; border: 1px solid #ddd;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Vista previa"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("get_thumbnail", "name", "location", "is_active", "edit_button")
    list_display_links = ("get_thumbnail", "name", "edit_button")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "location", "testimonial")
    list_editable = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"
    inlines = [ClientImageInline]
    exclude = ("testimonial_en", "latitude", "longitude")
    save_on_top = True

    def edit_button(self, obj):
        if obj.pk:
            url = reverse('admin:clients_client_change', args=[obj.pk])
            return format_html(
                '<a href="{}" class="edit-icon-link" title="Editar elemento">'
                '<i class="fas fa-pencil-alt"></i></a>',
                url
            )
        return "-"
    edit_button.short_description = "Acciones"

    fieldsets = (
        ("Información General", {
            "fields": (
                "name", 
                "slug", 
                "location", 
                "testimonial", 
                ("logo", "logo_preview"),
                ("cover", "cover_preview")
            )
        }),
        ("Configuración y Estado", {
            "fields": ("is_active",),
        }),
    )
    readonly_fields = ("logo_preview", "cover_preview")

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 8px; border: 1px solid #ddd;" />', obj.logo.url)
        return "No hay logo cargado"
    logo_preview.short_description = "Vista Previa del Logo"

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="width: 200px; height: auto; border-radius: 8px; border: 1px solid #ddd;" />', obj.cover.url)
        return "No hay portada cargada"
    cover_preview.short_description = "Vista Previa de la Portada"

    def get_thumbnail(self, obj):
        # Preferir el logo si existe
        if obj.logo:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 1px solid #ddd;" />', obj.logo.url)
        
        # Si no hay logo, intentar obtener la primera imagen de la galería
        first_image = obj.gallery.first()
        if first_image and first_image.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 1px solid #ddd;" />', first_image.image.url)
        return format_html('<div style="width: 45px; height: 45px; background: #eee; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #999;"><i class="fas fa-user"></i></div>')
    get_thumbnail.short_description = "Logo/Foto"

    @admin.action(description="Activar clientes seleccionados")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} clientes activados con éxito.")

    @admin.action(description="Desactivar clientes seleccionados")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} clientes desactivados con éxito.")
