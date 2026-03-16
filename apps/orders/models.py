from django.db import models
from django.contrib.auth import get_user_model
from apps.catalog.models import ProductVariant, Product

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente de Pago'),
        ('PAID', 'Pagado'),
        ('FAILED', 'Pago Fallido'),
        ('SHIPPED', 'Enviado'),
        ('DELIVERED', 'Entregado'),
        ('CANCELED', 'Cancelado'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario")
    session_id = models.CharField(max_length=255, null=True, blank=True, help_text="ID de sesión de pago o carrito anónimo")
    payment_reference = models.CharField(max_length=255, null=True, blank=True, help_text="Referencia de la pasarela de pagos")
    wompi_transaction_id = models.CharField(max_length=255, null=True, blank=True, help_text="ID de transacción en Wompi")
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Monto Total")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Estado")
    
    # Datos de envío
    contact_name = models.CharField(max_length=150, verbose_name="Nombre de contacto", blank=True, null=True)
    shipping_address = models.TextField(verbose_name="Dirección de envío", blank=True, null=True)
    contact_email = models.EmailField(verbose_name="Email de contacto", blank=True, null=True)
    contact_phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido #{self.id} - {self.get_status_display()}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Producto Principal")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Variante de Producto")
    product_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre Producto (Histórico)")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de compra (Unidad)")

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Items de Pedido"

    def __str__(self):
        if self.product_variant:
            name = str(self.product_variant)
        elif self.product:
            name = self.product.name
        elif self.product_name:
            name = self.product_name
        else:
            name = "Desconocido"
        return f"{self.quantity}x {name} (Pedido #{self.order.id})"
