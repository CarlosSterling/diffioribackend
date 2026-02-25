from django import template
from apps.catalog.models import Product, Category, ProductImage
from apps.clients.models import Client
from apps.blog.models import BlogPost

register = template.Library()

@register.simple_tag
def get_dashboard_metrics():
    return {
        "products_active": Product.objects.filter(is_active=True).count(),
        "products_inactive": Product.objects.filter(is_active=False).count(),
        "categories_count": Category.objects.count(),
        "clients_active": Client.objects.filter(is_active=True).count(),
        "blog_published": BlogPost.objects.filter(is_published=True).count(),
        "total_images": ProductImage.objects.count(),
    }
