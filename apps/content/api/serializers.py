from rest_framework import serializers
from ..models import HeroSlide, HomeAbout, HomeFeature, HomeCTA


def _media_url(obj, field):
    """Devuelve la URL relativa del campo imagen (ej: /media/hero/foto.png).
    Usar URL relativas evita que el dominio del servidor (localhost:8080 en dev,
    IP pública en prod) quede hardcodeado y genera problemas de "Load failed"
    cuando el cliente y el servidor resuelven localhost de forma distinta."""
    if field and hasattr(field, 'url'):
        return field.url  # Ej: /media/hero/slider-prep.png
    return None


class HeroSlideSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _media_url(obj, obj.image)

    class Meta:
        model = HeroSlide
        fields = "__all__"


class HomeAboutSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _media_url(obj, obj.image)

    class Meta:
        model = HomeAbout
        fields = "__all__"


class HomeFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeFeature
        fields = "__all__"


class HomeCTASerializer(serializers.ModelSerializer):
    background_image = serializers.SerializerMethodField()

    def get_background_image(self, obj):
        return _media_url(obj, obj.background_image)

    class Meta:
        model = HomeCTA
        fields = "__all__"
