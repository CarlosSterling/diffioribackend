from rest_framework import serializers
from apps.clients.models import Client, ClientImage


def _relative_url(field):
    if field:
        return field.url
    return None


class ClientImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _relative_url(obj.image)

    class Meta:
        model = ClientImage
        fields = ("id", "image", "alt", "alt_en")


class ClientSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    gallery = ClientImageSerializer(many=True, read_only=True)

    def get_logo(self, obj):
        return _relative_url(obj.logo)

    def get_cover(self, obj):
        return _relative_url(obj.cover)

    class Meta:
        model = Client
        fields = "__all__"

