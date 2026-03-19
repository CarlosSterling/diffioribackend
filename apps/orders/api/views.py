import hashlib
import requests as http_requests
from decimal import Decimal
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.emails import send_order_confirmation, notify_admin_new_order

from ..models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from apps.catalog.models import ProductVariant

WOMPI_MIN_AMOUNT_IN_CENTS = 150000


def _order_response(order):
    return {
        "order_id": order.id,
        "status": order.status,
        "total_amount": str(order.total_amount),
        "contact_name": order.contact_name,
        "contact_email": order.contact_email,
        "contact_phone": order.contact_phone,
        "shipping_address": order.shipping_address,
    }


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

            total = Decimal('0.00')
            valid_items = 0
            # Agregar items y calcular total
            for item in data['items']:
                v_id = item.get('variant_id')
                product_id = item.get('product_id')
                quantity = int(item.get('quantity', 1))

                variant = None
                price = Decimal('0.00')

                from django.core.exceptions import MultipleObjectsReturned
                try:
                    if str(v_id).isdigit():
                        variant = ProductVariant.objects.get(id=v_id)
                        price = variant.price
                        product = variant.product
                        product_name = f"{product.name} - {variant.weight} ({variant.grind})"
                    else:
                        variant = ProductVariant.objects.get(product__slug=v_id)
                        price = variant.price
                        product = variant.product
                        product_name = f"{product.name} - {variant.weight} ({variant.grind})"
                except (ProductVariant.DoesNotExist, ValueError, TypeError, MultipleObjectsReturned):
                    try:
                        from apps.catalog.models import Product
                        lookup_value = product_id if product_id not in (None, "") else v_id
                        if str(lookup_value).isdigit():
                            product = Product.objects.get(id=lookup_value)
                        else:
                            product = Product.objects.get(slug=lookup_value)
                        price = product.price or Decimal('0.00')
                        product_name = product.name
                        variant = None
                    except (Product.DoesNotExist, ValueError, TypeError):
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
                valid_items += 1

            if valid_items == 0 or total <= Decimal('0.00'):
                order.delete()
                return Response(
                    {"error": "No se pudieron validar los productos del carrito. Actualiza la pagina y vuelve a intentarlo."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order.total_amount = total
            order.save()

            # ── Crear Payment Link en Wompi ──────────────────────────
            wompi_base_url    = getattr(settings, 'WOMPI_BASE_URL', 'https://sandbox.wompi.co/v1')
            wompi_private_key = getattr(settings, 'WOMPI_PRIVATE_KEY', '')
            wompi_redirect    = getattr(settings, 'WOMPI_REDIRECT_URL', '')
            amount_in_cents   = int(total * 100)

            if amount_in_cents < WOMPI_MIN_AMOUNT_IN_CENTS:
                order.delete()
                return Response(
                    {
                        "error": "El valor minimo para pagar con Wompi es $1.500 COP. Agrega mas productos al carrito para continuar."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                wompi_resp = http_requests.post(
                    f"{wompi_base_url}/payment_links",
                    json={
                        "name": f"Pedido Diffiori #{order.id}",
                        "description": f"Compra en Diffiori Café - {order.contact_name}",
                        "single_use": True,
                        "currency": "COP",
                        "amount_in_cents": amount_in_cents,
                        "redirect_url": f"{wompi_redirect}?order_id={order.id}",
                        "collect_shipping": False,
                        "expires_in_minutes": 30,
                    },
                    headers={"Authorization": f"Bearer {wompi_private_key}"},
                    timeout=10,
                )
                wompi_resp.raise_for_status()
                wompi_data = wompi_resp.json()
                wompi_entry = wompi_data.get("data", {})
                # Wompi returns the checkout URL in "link"; fallback to constructing from id
                link_id = wompi_entry.get("id", "")
                payment_url = wompi_entry.get("link") or f"https://checkout.wompi.co/l/{link_id}"
                order.payment_reference = link_id
                order.save(update_fields=["payment_reference"])
            except http_requests.RequestException as e:
                error_body = ""
                if getattr(e, "response", None) is not None:
                    error_body = e.response.text
                order.delete()
                print(f"ERROR Wompi API: {e} BODY={error_body}")
                return Response(
                    {"error": "No fue posible crear el enlace de pago con Wompi. Revisa el valor del pedido e intenta de nuevo."},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            return Response({
                "order_id": order.id,
                "payment_url": payment_url,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def webhook(self, request):
        """
        Endpoint que recibe las notificaciones de Wompi.
        Valida la firma SHA256 con la events_key según la especificación de Wompi.
        """
        data = request.data

        # ── 1. Validar firma Wompi ─────────────────────────────
        sig               = data.get("signature", {})
        props             = sig.get("properties", [])
        checksum_received = sig.get("checksum", "")
        events_key        = getattr(settings, 'WOMPI_EVENTS_KEY', '')

        timestamp         = data.get("timestamp", "")
        concat_str = ""
        for prop in props:
            value = data.get("data", {})
            for part in prop.split("."):
                value = value.get(part, "") if isinstance(value, dict) else ""
            concat_str += str(value)
        concat_str += f"{timestamp}{events_key}"

        checksum_computed = hashlib.sha256(concat_str.encode("utf-8")).hexdigest()
        if checksum_computed != checksum_received:
            print(f"WEBHOOK: firma inválida. Esperado={checksum_computed}, recibido={checksum_received}")
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        # ── 2. Manejar evento ──────────────────────────────────
        event = data.get("event")
        if event == "transaction.updated":
            transaction  = data.get("data", {}).get("transaction", {})
            wompi_status = transaction.get("status", "")
            reference    = transaction.get("reference", "")   # = ID del payment link guardado en payment_reference
            wompi_tx_id  = transaction.get("id", "")

            STATUS_MAP = {
                "APPROVED": "PAID",
                "DECLINED": "FAILED",
                "VOIDED":   "CANCELED",
                "ERROR":    "FAILED",
            }
            order_status = STATUS_MAP.get(wompi_status)

            if order_status:
                try:
                    order = Order.objects.get(payment_reference=reference)
                except Order.DoesNotExist:
                    print(f"WEBHOOK: Orden no encontrada para reference={reference}")
                    return Response(status=status.HTTP_200_OK)

                # Idempotencia: no pisar estados finales
                if order.status in ("PAID", "SHIPPED", "DELIVERED"):
                    return Response(status=status.HTTP_200_OK)

                order.status = order_status
                order.wompi_transaction_id = wompi_tx_id
                order.save(update_fields=["status", "wompi_transaction_id"])

                if order.status == "PAID":
                    send_order_confirmation(order)
                    notify_admin_new_order(order)

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='new-paid')
    def new_paid(self, request):
        """Devuelve pedidos PAID con id > since_id. Solo para staff del admin."""
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        since_id = int(request.query_params.get('since_id', 0))
        orders = Order.objects.filter(status='PAID', id__gt=since_id).values('id', 'contact_name', 'total_amount')
        return Response({"orders": list(orders)})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='verify-payment')
    def verify_payment(self, request):
        """
        Consulta el estado de una transacción en Wompi y actualiza la orden.
        Body: { "wompi_transaction_id": "...", "order_id": 123 }
        """
        wompi_tx_id = request.data.get("wompi_transaction_id", "")
        order_id    = request.data.get("order_id")

        if not wompi_tx_id or not order_id:
            return Response({"error": "wompi_transaction_id and order_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Idempotencia: si ya tiene estado final no consultamos de nuevo
        if order.status in ("PAID", "SHIPPED", "DELIVERED", "FAILED", "CANCELED"):
            return Response(_order_response(order))

        wompi_base_url    = getattr(settings, 'WOMPI_BASE_URL', 'https://sandbox.wompi.co/v1')
        wompi_private_key = getattr(settings, 'WOMPI_PRIVATE_KEY', '')

        try:
            resp = http_requests.get(
                f"{wompi_base_url}/transactions/{wompi_tx_id}",
                headers={"Authorization": f"Bearer {wompi_private_key}"},
                timeout=10,
            )
            resp.raise_for_status()
            tx_data = resp.json().get("data", {})
        except http_requests.RequestException as e:
            print(f"ERROR verify-payment Wompi: {e}")
            return Response({"error": "No se pudo consultar Wompi"}, status=status.HTTP_502_BAD_GATEWAY)

        wompi_status = tx_data.get("status", "")
        STATUS_MAP = {
            "APPROVED": "PAID",
            "DECLINED": "FAILED",
            "VOIDED":   "CANCELED",
            "ERROR":    "FAILED",
        }
        new_status = STATUS_MAP.get(wompi_status)
        if new_status and new_status != order.status:
            order.status = new_status
            order.wompi_transaction_id = wompi_tx_id
            order.save(update_fields=["status", "wompi_transaction_id"])
            if order.status == "PAID":
                send_order_confirmation(order)
                notify_admin_new_order(order)

        return Response(_order_response(order))

    @action(detail=True, methods=['get'], permission_classes=[AllowAny], url_path='status')
    def order_status(self, _request, pk=None):
        """
        Devuelve el estado actual de una orden por ID.
        Usado por la página /checkout/return para verificar el resultado del pago.
        """
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(_order_response(order))
