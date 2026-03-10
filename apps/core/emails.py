import resend
import os
from django.conf import settings
from django.template.loader import render_to_string

# Configuramos la API Key leyendo directamente del entorno del sistema
resend.api_key = os.environ.get("RESEND_API_KEY")

def send_order_confirmation(order):
    try:
        html_content = render_to_string("emails/order_confirmation.html", {"order": order})
        
        params = {
            "from": os.environ.get("DEFAULT_FROM_EMAIL"),
            "to": [order.contact_email],
            "subject": f"☕ ¡Tu pedido #{order.id} está en camino! - Diffiori Café",
            "html": html_content,
        }
        
        result = resend.Emails.send(params)
        print(f"DEBUG EMAIL CLIENTE: {result}")
        return result
    except Exception as e:
        print(f"❌ ERROR RESEND CLIENTE: {e}")
        return None

def notify_admin_new_order(order):
    try:
        admin_email = os.environ.get("ADMIN_EMAIL")
        html_content = render_to_string("emails/admin_new_order.html", {"order": order})
        
        params = {
            "from": os.environ.get("DEFAULT_FROM_EMAIL"),
            "to": [admin_email],
            "subject": f"🚨 NUEVA VENTA: Pedido #{order.id}",
            "html": html_content,
        }
        
        result = resend.Emails.send(params)
        print(f"DEBUG EMAIL ADMIN: {result}")
        return result
    except Exception as e:
        print(f"❌ ERROR RESEND ADMIN: {e}")
        return None
