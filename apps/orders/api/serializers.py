from rest_framework import serializers
from ..models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'session_id', 'total_amount', 'status', 
            'shipping_address', 'contact_email', 'contact_phone', 
            'created_at', 'items'
        ]
        read_only_fields = ['id', 'user', 'total_amount', 'status', 'created_at']

class CheckoutSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField()
    )
    contact_email = serializers.EmailField()
    shipping_address = serializers.CharField(max_length=500)
    contact_phone = serializers.CharField(max_length=50)
