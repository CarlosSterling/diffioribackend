import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_viva.settings')
django.setup()

from apps.content.models import HeroSlide, HomeAbout, HomeFeature, HomeCTA

def migrate_home_content():
    print("Migrating simplified homepage content (Spanish Only)...")

    # 1. Hero Slides
    hero_slides = [
        {
            "title": "Arte con Sabor a Café!",
            "subtitle": "Somos una cafetería que combina la pasión por el buen café con el arte y la cultura local. Más que un lugar para disfrutar de una bebida, somos un espacio de encuentro donde convergen sabores, aromas, creatividad y calidez.",
            "order": 1,
            "image": "hero/slider-prep.png"
        },
        {
            "title": "Capuchinos Perfectos",
            "subtitle": "Textura sedosa y arte latte que deleitan tus sentidos en cada sorbo.",
            "order": 2,
            "image": "hero/slider-capuchino.png"
        },
        {
            "title": "Malteadas de Especialidad",
            "subtitle": "Una explosión de frescura y sabor con nuestra base de café premium.",
            "order": 3,
            "image": "hero/slider-milkshake.png"
        },
        {
            "title": "Café por Libra",
            "subtitle": "Lleva a casa la esencia del Huila, tostado a la perfección para tu hogar.",
            "order": 4,
            "image": "hero/slider-pound.png"
        }
    ]

    for slide in hero_slides:
        HeroSlide.objects.get_or_create(
            title=slide["title"],
            defaults={
                "subtitle": slide["subtitle"],
                "order": slide["order"],
                "image": slide["image"]
            }
        )

    # 2. Home About
    about_data = {
        "title": "Sobre Nosotros",
        "description": "Somos una empresa apasionada por el café de origen del Huila. Trabajamos de la mano con caficultores locales para llevar el sabor de nuestra tierra a cada taza. Nuestra misión es resaltar la calidad y el esfuerzo de quienes cultivan lo mejor de nuestro campo.",
        "long_description": "Nuestra historia comienza en las montañas del Huila, donde cada grano de café es cultivado con pasión y tradición. \n\nTrabajamos de la mano con caficultores locales para asegurar un comercio justo y prácticas sostenibles. Cada taza que tomas apoya a una comunidad dedicada a la excelencia.\n\nEn Diffiori, creemos que el café es más que una bebida; es un ritual que conecta personas. Desde la selección del grano hasta el tostado, cada paso es cuidadosamente monitoreado para ofrecerte una experiencia sensorial inigualable.",
        "cta_text": "Leer nuestra historia completa",
        "image": "about/coffee-farm-huila-hero.png"
    }
    
    HomeAbout.objects.get_or_create(
        title=about_data["title"],
        defaults=about_data
    )

    # 3. Home Features
    features = [
        {
            "icon": "Coffee",
            "title": "Café de Especialidad",
            "description": "Seleccionamos granos con puntaje SCA superior a 80, destacados por su complejidad de sabor y origen.",
            "order": 1
        },
        {
            "icon": "Award",
            "title": "Calidad Premium",
            "description": "Cada lote pasa por control riguroso de calidad antes de llegar a tu taza.",
            "order": 2
        },
        {
            "icon": "Leaf",
            "title": "Origen Directo",
            "description": "Trabajamos directamente con familias caficultoras del Huila, Colombia, apoyando el comercio justo.",
            "order": 3
        }
    ]

    for feature in features:
        HomeFeature.objects.get_or_create(
            title=feature["title"],
            defaults=feature
        )

    # 4. Home CTA
    cta_data = {
        "title": "Vive la Experiencia Diffiori",
        "subtitle": "Visítanos y descubre por qué somos mucho más que una cafetería.",
        "cta_text": "Visítanos",
        "cta_link": "/#footer",
        "background_image": "cta/coffee-farm-hero.png"
    }

    HomeCTA.objects.get_or_create(
        title=cta_data["title"],
        defaults=cta_data
    )

    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_home_content()
