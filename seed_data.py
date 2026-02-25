import os
import django
from django.utils import timezone
from apps.clients.models import Client
from apps.blog.models import BlogPost

# Delete existing data to clean up "prueba" entries
print("Cleaning existing data...")
Client.objects.all().delete()
BlogPost.objects.all().delete()

# --- Create Clients ---
clients_data = [
    {
        "name": "Cafetería Central",
        "testimonial": "El café de Diffiori ha transformado nuestra oferta. Nuestros clientes notan la diferencia en cada taza.",
        "location": "Bogotá, Colombia",
        # We can't easily upload images from script without files, so we leave them empty for now.
        # The user can update them in admin.
    },
    {
        "name": "Hotel Plaza",
        "testimonial": "Calidad premium constante. El servicio y el producto son excepcionales para nuestro buffet de desayuno.",
        "location": "Medellín, Colombia",
    },
    {
        "name": "Restaurante El Mirador",
        "testimonial": "Buscábamos un café con identidad y Diffiori nos dio exactamente eso. Un perfil de taza único.",
        "location": "Cartagena, Colombia",
    }
]

print("Creating Clients...")
for c_data in clients_data:
    Client.objects.create(
        name=c_data["name"],
        testimonial=c_data["testimonial"],
        location=c_data["location"],
        is_active=True
    )

# --- Create Blog Posts ---
posts_data = [
    {
        "title": "Beneficios del Café de Especialidad",
        "excerpt": "Descubre por qué el café de especialidad no solo sabe mejor, sino que es mejor para ti y para el planeta.",
        "content": "<p>El café de especialidad se distingue por su cuidado en cada etapa, desde el cultivo hasta la taza.</p><p>A diferencia del café comercial, los granos de especialidad son seleccionados manualmente y tostados para resaltar sus notas únicas.</p>",
    },
    {
        "title": "Métodos de Preparación: V60",
        "excerpt": "Aprende a preparar una taza limpia y aromática usando el método de vertido V60.",
        "content": "<p>El V60 es uno de los métodos favoritos de los baristas por su capacidad para producir una taza limpia y compleja.</p><p>Necesitarás: 20g de café, 300ml de agua a 93°C, y un filtro de papel.</p>",
    },
    {
        "title": "Historia del Café en el Huila",
        "excerpt": "Un viaje a través de las montañas del Huila para entender por qué produce algunos de los mejores cafés del mundo.",
        "content": "<p>El departamento del Huila es reconocido mundialmente por su café de alta calidad.</p><p>Su geografía montañosa y suelos volcánicos crean el microclima perfecto para el cultivo de variedades como Caturra y Castillo.</p>",
    }
]

print("Creating Blog Posts...")
for p_data in posts_data:
    BlogPost.objects.create(
        title=p_data["title"],
        excerpt=p_data["excerpt"],
        content=p_data["content"],
        cover_image="", # Placeholder
        published_at=timezone.now(),
        is_published=True
    )

print("Database seeded successfully!")
