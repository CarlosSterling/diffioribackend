from rest_framework import serializers
from apps.clients.models import Client, ClientImage


class ClientImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get("request")
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = ClientImage
        fields = ("id", "image", "alt")


class ClientSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    gallery = ClientImageSerializer(many=True, read_only=True)

    def _abs(self, field):
        request = self.context.get("request")
        if request and field:
            return request.build_absolute_uri(field.url)
        return None

    def get_logo(self, obj):
        return self._abs(obj.logo)

    def get_cover(self, obj):
        return self._abs(obj.cover)

    class Meta:
        model = Client
        fields = "__all__"
