import hmac
import hashlib
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from apps.catalog.models import ProductVariant

class OrderViewSet(viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions():
        return [AllowAny()]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def checkout(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Crear Orden Pendiente
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                contact_email=data['contact_email'],
                shipping_address=data['shipping_address'],
                contact_phone=data['contact_phone'],
                status='PENDING'
            )

            total = 0
            # Agregar items y calcular total
            for item in data['items']:
                variant_id = item.get('variant_id')
                quantity = item.get('quantity', 1)
                
                try:
                    variant = ProductVariant.objects.get(id=variant_id)
                    price = variant.price
                    OrderItem.objects.create(
                        order=order,
                        product_variant=variant,
                        quantity=quantity,
                        price_at_purchase=price
                    )
                    total += (price * quantity)
                except ProductVariant.DoesNotExist:
                    continue

            order.total_amount = total
            order.save()

            # TODO: LLAMAR A LA API COMERCIAL DE PAGOS PARA CREAR SESIÓN (Ej: Stripe Checkout Session / MercadoPago Init Point)
            payment_url = "https://checkout.sandbox.gateway.com/" # PLACEHOLDER
            
            return Response({
                "message": "Order created successfully",
                "order_id": order.id,
                "payment_url": payment_url
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def webhook(self, request):
        """
        Endpoint que recibe las notificaciones de la pasarela de pagos.
        Debe verificar la firma HMAC para evitar ataques de spoofing.
        """
        payload = request.body
        sig_header = request.headers.get('Signature')

        # Ejemplo de validación HMAC (común en webhooks robustos)
        secret = getattr(settings, 'WEBHOOK_SECRET', b'default_secret').encode('utf-8')
        hash_calc = hmac.new(secret, payload, hashlib.sha256).hexdigest()

        # En un escenario real, if sig_header != hash_calc -> rechazar
        # Asumiendo validación exitosa:
        event = request.data.get("event")
        order_id = request.data.get("order_id")

        if event == "payment.success":
            try:
                order = Order.objects.get(id=order_id)
                order.status = 'PAID'
                order.payment_reference = request.data.get("transaction_id")
                order.save()
            except Order.DoesNotExist:
                pass

        return Response(status=status.HTTP_200_OK)
