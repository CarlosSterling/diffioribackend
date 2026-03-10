from rest_framework import viewsets, permissions, filters
from apps.catalog.models import Product, Category
from . import serializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ("name", "short_desc", "description")
    ordering_fields = ("created_at", "price", "sort_order")
    ordering = ["sort_order", "created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        # ?favorites=true → solo productos favoritos (para la sección "Nuestros Favoritos")
        if self.request.query_params.get("favorites", "").lower() in ("true", "1"):
            qs = qs.filter(is_favorite=True)
        return qs
