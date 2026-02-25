from apps.clients.models import Client
from apps.blog.models import BlogPost
from django.utils import timezone

def populate():
    # --- Clientes ---
    clients_data = [
        {"name": "Café Maravilla", "testimonial": "El mejor café que hemos servido en nuestro establecimiento.", "location": "Bogotá, Colombia"},
        {"name": "Panadería El Sol", "testimonial": "Calidad inigualable y un servicio excepcional.", "location": "Pitalito, Huila"},
        {"name": "Hotel del Valle", "testimonial": "Nuestros huéspedes siempre comentan sobre el aroma.", "location": "Neiva, Huila"}
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
        if created: print(f"Cliente creado: {client.name}")

    # --- Blog ---
    blog_data = [
        {"title": "El Arte del Tueste Perfecto", "excerpt": "Descubre los secretos detrás de un café con cuerpo.", "content": "Contenido ejemplo...", "is_published": True},
        {"title": "Historia de Diffiori en Pitalito", "excerpt": "Nuestros inicios y el compromiso con la tierra.", "content": "Contenido ejemplo...", "is_published": True},
        {"title": "Guía de Preparación: Prensa Francesa", "excerpt": "Aprende a preparar una taza perfecta.", "content": "Contenido ejemplo...", "is_published": True}
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
        if created: print(f"Blog post creado: {post.title}")

populate()
