from rest_framework import viewsets
from ..models import HeroSlide, HomeAbout, HomeFeature, HomeCTA
from .serializers import (
    HeroSlideSerializer, 
    HomeAboutSerializer, 
    HomeFeatureSerializer, 
    HomeCTASerializer
)

class HeroSlideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HeroSlide.objects.filter(is_active=True)
    serializer_class = HeroSlideSerializer

class HomeAboutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomeAbout.objects.all()
    serializer_class = HomeAboutSerializer

    def get_object(self):
        return self.get_queryset().first()

class HomeFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomeFeature.objects.filter(is_active=True)
    serializer_class = HomeFeatureSerializer

class HomeCTAViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomeCTA.objects.all()
    serializer_class = HomeCTASerializer

    def get_object(self):
        return self.get_queryset().first()
