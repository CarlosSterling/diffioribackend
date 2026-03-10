from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import HeroSlide, HomeAbout, HomeFeature, HomeCTA

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("get_thumbnail", "title", "order", "is_active", "edit_button")
    list_display_links = ("get_thumbnail", "title", "edit_button")
    list_editable = ("order", "is_active")
    search_fields = ("title",)
    # exclude = ("title_en", "subtitle_en", "button_text_en")
    readonly_fields = ("button_link",)
    save_on_top = True
 
    def edit_button(self, obj):
        if obj.pk:
            url = reverse('admin:content_heroslide_change', args=[obj.pk])
            return format_html(
                '<a href="{}" class="edit-icon-link" title="Editar elemento">'
                '<i class="fas fa-pencil-alt"></i></a>',
                url
            )
        return "-"
    edit_button.short_description = "Acciones"

    fieldsets = (
        ("Imagen y Configuración", {
            "fields": ("image", "button_link", "order", "is_active")
        }),
        ("Contenido (Español)", {
            "fields": ("title", "subtitle", "button_text")
        }),
        ("Contenido (Inglés)", {
            "fields": ("title_en", "subtitle_en", "button_text_en")
        }),
    )

    def get_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height: 45px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />', obj.image.url)
        return "-"
    get_thumbnail.short_description = "Miniatura"

@admin.register(HomeAbout)
class HomeAboutAdmin(admin.ModelAdmin):
    list_display = ("get_thumbnail", "title", "edit_button")
    list_display_links = ("get_thumbnail", "title", "edit_button")
    # exclude = ("title_en", "description_en", "long_description_en", "cta_text_en")
    save_on_top = True

    def edit_button(self, obj):
        if obj.pk:
            url = reverse('admin:content_homeabout_change', args=[obj.pk])
            return format_html(
                '<a href="{}" class="edit-icon-link" title="Editar elemento">'
                '<i class="fas fa-pencil-alt"></i></a>',
                url
            )
        return "-"
    edit_button.short_description = "Acciones"

    fieldsets = (
        ("Imagen", {
            "fields": ("image",)
        }),
        ("Contenido (Español)", {
            "fields": ("title", "description", "long_description", "cta_text")
        }),
        ("Contenido (Inglés)", {
            "fields": ("title_en", "description_en", "long_description_en", "cta_text_en")
        }),
    )

    def get_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />', obj.image.url)
        return "-"
    get_thumbnail.short_description = "Miniatura"

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(HomeFeature)
class HomeFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active", "edit_button")
    list_display_links = ("title", "edit_button")
    list_editable = ("order", "is_active")
    # exclude = ("title_en", "description_en", "value")
    save_on_top = True

    def edit_button(self, obj):
        if obj.pk:
            url = reverse('admin:content_homefeature_change', args=[obj.pk])
            return format_html(
                '<a href="{}" class="edit-icon-link" title="Editar elemento">'
                '<i class="fas fa-pencil-alt"></i></a>',
                url
            )
        return "-"
    edit_button.short_description = "Acciones"

    fieldsets = (
        ("Configuración", {
            "fields": ("icon", "order", "is_active")
        }),
        ("Contenido (Español)", {
            "fields": ("title", "description")
        }),
        ("Contenido (Inglés)", {
            "fields": ("title_en", "description_en")
        }),
    )

@admin.register(HomeCTA)
class HomeCTAAdmin(admin.ModelAdmin):
    list_display = ("title", "cta_link", "actions_buttons")
    list_display_links = ("title",)
    # exclude = ("title_en", "subtitle_en", "cta_text_en")
    save_on_top = True

    def actions_buttons(self, obj):
        if obj.pk:
            edit_url = reverse('admin:content_homecta_change', args=[obj.pk])
            delete_url = reverse('admin:content_homecta_delete', args=[obj.pk])
            return format_html(
                '<a href="{}" class="edit-icon-link" title="Editar elemento">'
                '<i class="fas fa-pencil-alt"></i></a>'
                '&nbsp;&nbsp;'
                '<a href="{}" class="delete-icon-link" title="Eliminar elemento" '
                'style="color: #8B3D30;">'
                '<i class="fas fa-trash-alt"></i></a>',
                edit_url, delete_url
            )
        return "-"
    actions_buttons.short_description = "Acciones"

    fieldsets = (
        ("Configuración", {
            "fields": ("cta_link", "background_image")
        }),
        ("Contenido (Español)", {
            "fields": ("title", "subtitle", "cta_text")
        }),
        ("Contenido (Inglés)", {
            "fields": ("title_en", "subtitle_en", "cta_text_en")
        }),
    )
