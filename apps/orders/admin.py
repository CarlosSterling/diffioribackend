from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_variant', 'product_name', 'quantity', 'price_at_purchase')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_name', 'total_amount', 'get_products', 'status_colored', 'contact_phone', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'contact_name', 'contact_email', 'contact_phone', 'payment_reference', 'wompi_transaction_id')
    readonly_fields = ('user', 'total_amount', 'created_at', 'updated_at', 'payment_reference', 'session_id', 'wompi_transaction_id')
    inlines = [OrderItemInline]
    
    def get_products(self, obj):
        return ", ".join([str(item) for item in obj.items.all()])
    get_products.short_description = "Productos"

    def status_colored(self, obj):
        from django.utils.html import format_html
        colors = {
            'PENDING': '#FFA500',  # Orange
            'PAID': '#28A745',     # Green
            'FAILED': '#DC3545',   # Red
            'SHIPPED': '#007BFF',  # Blue
            'DELIVERED': '#6C757D', # Gray
            'CANCELED': '#343A40',  # Dark
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; border-radius: 10px; font-weight: bold; font-size: 10px;">{}</span>',
            colors.get(obj.status, '#000'),
            obj.get_status_display()
        )
    status_colored.short_description = "Estado"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'get_order', 'get_product_name', 'quantity', 'price_at_purchase', 'get_order_total')
    list_filter = ('order__status', 'order__created_at')
    ordering = ('-order__id', 'id')

    def get_product_name(self, obj):
        return str(obj).split('x ', 1)[-1].split(' (Pedido')[0]
    get_product_name.short_description = "Producto"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order')

    def is_first_item(self, obj):
        # Cache the first item ID of the order to avoid redundant queries in larger lists
        if not hasattr(self, '_first_item_cache'):
            self._first_item_cache = {}
        
        if obj.order_id not in self._first_item_cache:
            first_id = OrderItem.objects.filter(order_id=obj.order_id).order_by('id').values_list('id', flat=True).first()
            self._first_item_cache[obj.order_id] = first_id
            
        return obj.id == self._first_item_cache[obj.order_id]

    def get_id(self, obj):
        return obj.id if self.is_first_item(obj) else ""
    get_id.short_description = "ID"

    def get_order(self, obj):
        return f"Pedido #{obj.order.id}" if self.is_first_item(obj) else ""
    get_order.short_description = "Orden"
    
    def get_order_total(self, obj):
        return obj.order.total_amount if self.is_first_item(obj) else ""
    get_order_total.short_description = "Total Pedido"
