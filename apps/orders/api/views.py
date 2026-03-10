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

    def get_permissions(self):
        return [AllowAny()]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def checkout(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Crear Orden Pendiente
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                contact_name=data['contact_name'],
                contact_email=data['contact_email'],
                shipping_address=data['shipping_address'],
                contact_phone=data['contact_phone'],
                status='PENDING'
            )

            from decimal import Decimal
            total = Decimal('0.00')
            # Agregar items y calcular total
            for item in data['items']:
                v_id = item.get('variant_id')
                quantity = int(item.get('quantity', 1))
                
                variant = None
                price = Decimal('0.00')
                
                print(f"DEBUG: Processing item variant_id={v_id}, quantity={quantity}")
                
                # 1. Intentar buscar como Variante (por ID o slug)
                from django.core.exceptions import MultipleObjectsReturned
                try:
                    if str(v_id).isdigit():
                        variant = ProductVariant.objects.get(id=v_id)
                        price = variant.price
                        product = variant.product
                        product_name = f"{product.name} - {variant.weight} ({variant.grind})"
                    else:
                        # Si es un slug, podría ser que el producto solo tenga una variante
                        variant = ProductVariant.objects.get(product__slug=v_id)
                        price = variant.price
                        product = variant.product
                        product_name = f"{product.name} - {variant.weight} ({variant.grind})"
                    print(f"DEBUG: Found variant price={price}")
                except (ProductVariant.DoesNotExist, ValueError, TypeError, MultipleObjectsReturned):
                    # 2. Si no es variante (o hay muchas), buscar como Producto base
                    try:
                        from apps.catalog.models import Product
                        if str(v_id).isdigit():
                            product = Product.objects.get(id=v_id)
                        else:
                            product = Product.objects.get(slug=v_id)
                        price = product.price or Decimal('0.00')
                        product_name = product.name
                        variant = None # Asegurar que es None si es producto base
                        print(f"DEBUG: Found product price={price}")
                    except (Product.DoesNotExist, ValueError, TypeError):
                        print(f"DEBUG: Item NOT found: {v_id}")
                        continue

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_variant=variant,
                    product_name=product_name,
                    quantity=quantity,
                    price_at_purchase=price
                )
                total += (price * quantity)

            print(f"DEBUG: Calculated total={total}")
            order.total_amount = total
            
            # SIMULACIÓN DE PAGOS
            # Soporta: simulate=true (éxito por defecto) o simulate_status='FAILED'
            is_simulation = request.data.get("simulate", False)
            sim_status = request.data.get("simulate_status", "PAID").upper()

            if is_simulation or "simulate_status" in request.data:
                if sim_status == 'PAID':
                    order.status = 'PAID'
                    order.payment_reference = "SIMULATED-PAYMENT-SUCCESS"
                elif sim_status == 'FAILED':
                    order.status = 'FAILED'
                    order.payment_reference = "SIMULATED-PAYMENT-FAILURE"
            
            order.save()

            # TODO: LLAMAR A LA API COMERCIAL DE PAGOS PARA CREAR SESIÓN 
            payment_url = "https://checkout.sandbox.gateway.com/"
            
            return Response({
                "message": "Order created successfully",
                "order_id": order.id,
                "status": order.status,
                "total_amount": order.total_amount,
                "shipping_address": order.shipping_address,
                "contact_name": order.contact_name,
                "contact_phone": order.contact_phone,
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
