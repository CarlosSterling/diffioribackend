from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from apps.catalog.models import Product, ProductImage, Category, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "edit_button")
    list_display_links = ("name", "edit_button")
    # exclude = ("name_en",)
    fields = ("name", "name_en", "slug", "order", "get_frontend_url")
    readonly_fields = ("get_frontend_url",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "name_en")
    save_on_top = True

    def edit_button(self, obj):
        if obj.pk:
            url = reverse('admin:catalog_category_change', args=[obj.pk])
            return format_html(
                '<a href="{}" class="edit-icon-link" title="Editar elemento">'
                '<i class="fas fa-pencil-alt"></i></a>',
                url
            )
        return "-"
    edit_button.short_description = "Acciones"

    def get_frontend_url(self, obj):
        if obj.id:
            url = f"/productos?category={obj.slug}"
            return format_html('<code style="background: #f4efee; padding: 4px 8px; border-radius: 4px; color: #8B3D30; font-weight: bold;">{}</code>', url)
        return "-"
    get_frontend_url.short_description = "Enlace en la Web (Solo lectura)"


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ("weight", "weight_en", "grind", "grind_en", "price", "stock", "is_active")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt", "alt_en", "thumbnail")
    readonly_fields = ("thumbnail",)

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto; border-radius: 4px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Vista previa"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline]
    list_display = ("get_thumbnail", "name", "category", "price", "stock", "is_favorite", "is_active", "edit_button")
    list_display_links = ("get_thumbnail", "name")
    list_filter = ("category", "is_active", "is_favorite", "created_at")
    search_fields = ("name", "short_desc", "description")
    list_editable = ("price", "stock", "is_favorite", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"
    actions = ["make_active", "make_inactive", "duplicate_product"]
    # exclude = ("name_en", "short_desc_en", "description_en")
    save_on_top = True
    readonly_fields = ("cover_preview",)

    def edit_button(self, obj):
        if obj.pk:
            url = reverse('admin:catalog_product_change', args=[obj.pk])
            return format_html(
                '<a href="{}" class="edit-icon-link" title="Editar elemento">'
                '<i class="fas fa-pencil-alt"></i></a>',
                url
            )
        return "-"
    edit_button.short_description = "Acciones"
    
    fieldsets = (
        ("Información Básica (Español)", {
            "fields": ("name", "short_desc", "description")
        }),
        ("Información Básica (Inglés)", {
            "fields": ("name_en", "short_desc_en", "description_en")
        }),
        ("Configuración Técnica", {
            "fields": ("slug", "category", ("cover", "cover_preview"), ("price", "stock"), "data_sheet")
        }),
        ("Destacado y Estado", {
            "fields": ("is_favorite", "is_active"),
        }),
    )

    def get_thumbnail(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd;" />', obj.cover.url)
        return format_html('<div style="width: 45px; height: 45px; background: #eee; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #999;">N/A</div>')
    get_thumbnail.short_description = "Miniatura"

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />', obj.cover.url)
        return "No hay imagen seleccionada"
    cover_preview.short_description = "Vista Previa de la Portada"


    @admin.action(description="Activar productos seleccionados")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} productos activados con éxito.")

    @admin.action(description="Desactivar productos seleccionados")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} productos desactivados con éxito.")

    @admin.action(description="Duplicar productos seleccionados")
    def duplicate_product(self, request, queryset):
        for product in queryset:
            # Crear copia del producto
            product_images = product.gallery.all()
            product.pk = None
            product.name = f"{product.name} (Copia)"
            product.slug = "" # Forzar regeneración en save()
            product.is_active = False # Empezar desactivado para revisar
            product.save()

            # Duplicar imágenes de la galería
            for img in product_images:
                img.pk = None
                img.product = product
                img.save()
        
        self.message_user(request, f"{queryset.count()} productos duplicados. Por favor revise y active los borradores.")


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "weight", "grind", "price", "stock", "is_active")
    list_filter = ("is_active", "grind")
    search_fields = ("product__name", "weight")
