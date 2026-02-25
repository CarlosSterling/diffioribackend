from rest_framework import serializers
from apps.catalog.models import Product, ProductImage, Category, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get("request")
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = ProductImage
        fields = ("id", "image", "alt")


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ("id", "weight", "grind", "price", "stock", "is_active")


class ProductSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    category_slug = serializers.ReadOnlyField(source="category.slug")
    gallery = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    def get_cover(self, obj):
        request = self.context.get("request")
        if request and obj.cover:
            return request.build_absolute_uri(obj.cover.url)
        return None

    class Meta:
        model = Product
        fields = "__all__"
