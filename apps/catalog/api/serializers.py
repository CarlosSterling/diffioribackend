from rest_framework import serializers
from apps.catalog.models import Product, ProductImage, Category, ProductVariant


def _relative_url(field):
    """Devuelve la URL relativa del campo imagen (ej: /media/products/cover/foto.png).
    URLs relativas = sin dominio hardcodeado → funciona en dev y producción."""
    if field:
        return field.url  # /media/...
    return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _relative_url(obj.image)

    class Meta:
        model = ProductImage
        fields = ("id", "image", "alt", "alt_en")


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ("id", "weight", "weight_en", "grind", "grind_en", "price", "stock", "is_active")


class ProductSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    category_slug = serializers.ReadOnlyField(source="category.slug")
    category_name = serializers.ReadOnlyField(source="category.name")
    category_name_en = serializers.ReadOnlyField(source="category.name_en")
    gallery = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    def get_cover(self, obj):
        return _relative_url(obj.cover)

    class Meta:
        model = Product
        fields = "__all__"
