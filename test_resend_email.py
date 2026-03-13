import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_viva.settings')
django.setup()

from apps.orders.models import Order
from apps.core.emails import send_order_confirmation, notify_admin_new_order

# Get the latest order
order = Order.objects.order_by('-id').first()
if order:
    print(f"Order ID: {order.id}, Contact Email: {order.contact_email}")
    res = send_order_confirmation(order)
    print("Send to user returned:", res)
else:
    print("No order found")
