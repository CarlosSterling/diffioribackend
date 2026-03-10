from django import template
from django.db.models import Sum
from apps.catalog.models import Product, Category, ProductImage
from apps.clients.models import Client
from apps.blog.models import BlogPost
from apps.orders.models import Order

register = template.Library()

@register.simple_tag
def get_dashboard_metrics():
    # Only count Paid/Shipped/Delivered for total sales
    paid_orders = Order.objects.filter(status__in=['PAID', 'SHIPPED', 'DELIVERED'])
    total_sales = paid_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Simple manual formatting for currency as fallback to humanize
    total_sales_fmt = f"{int(total_sales):,}".replace(",", ".")

    return {
        "products_active": Product.objects.filter(is_active=True).count(),
        "products_inactive": Product.objects.filter(is_active=False).count(),
        "categories_count": Category.objects.count(),
        "clients_active": Client.objects.filter(is_active=True).count(),
        "blog_published": BlogPost.objects.filter(is_published=True).count(),
        "total_images": ProductImage.objects.count(),
        "orders_count": Order.objects.count(),
        "total_sales": total_sales,
        "total_sales_fmt": f"${total_sales_fmt}",
    }
