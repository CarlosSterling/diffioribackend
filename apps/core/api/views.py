from rest_framework import viewsets, permissions
from apps.core.models import FAQ
from . import serializers


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = serializers.FAQSerializer
    permission_classes = [permissions.AllowAny]
