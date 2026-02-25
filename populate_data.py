from apps.clients.models import Client
from apps.blog.models import BlogPost
from django.utils import timezone
import os

def populate():
    # --- Clientes ---
    clients_data = [
        {
            "name": "Café Maravilla",
            "testimonial": "El mejor café que hemos servido en nuestro establecimiento. Nuestros clientes están encantados.",
            "location": "Bogotá, Colombia"
        },
        {
            "name": "Panadería El Sol",
            "testimonial": "Calidad inigualable y un servicio excepcional. Un socio clave para nuestro negocio.",
            "location": "Pitalito, Huila"
        },
        {
            "name": "Hotel del Valle",
            "testimonial": "Nuestros huéspedes siempre comentan sobre el aroma y sabor del café Diffiori.",
            "location": "Neiva, Huila"
        }
    ]

    for data in clients_data:
        client, created = Client.objects.get_or_create(
            name=data["name"],
            defaults={
                "testimonial": data["testimonial"],
                "location": data["location"],
                "is_active": True
            }
        )
        if created:
            print(f"Cliente creado: {client.name}")

    # --- Blog ---
    blog_data = [
        {
            "title": "El Arte del Tueste Perfecto",
            "excerpt": "Descubre los secretos detrás de un café con cuerpo y sabor equilibrado.",
            "content": "El proceso de tueste es fundamental para liberar los aceites y aromas... (Ejemplo de contenido)",
            "is_published": True
        },
        {
            "title": "Historia de Diffiori en Pitalito",
            "excerpt": "Nuestros inicios y el compromiso con la tierra del mejor café.",
            "content": "Diffiori nació de la pasión por el café de alta calidad en el corazón del Huila... (Ejemplo de contenido)",
            "is_published": True
        },
        {
            "title": "Guía de Preparación: Prensa Francesa",
            "excerpt": "Aprende a preparar una taza perfecta en casa con esta técnica clásica.",
            "content": "La prensa francesa permite extraer los sabores más profundos del grano... (Ejemplo de contenido)",
            "is_published": True
        }
    ]

    for data in blog_data:
        post, created = BlogPost.objects.get_or_create(
            title=data["title"],
            defaults={
                "excerpt": data["excerpt"],
                "content": data["content"],
                "published_at": timezone.now(),
                "is_published": data["is_published"]
            }
        )
        if created:
            print(f"Blog post creado: {post.title}")

if __name__ == "__main__":
    populate()
