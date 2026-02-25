from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import (
    HeroSlideViewSet,
    HomeAboutViewSet,
    HomeFeatureViewSet,
    HomeCTAViewSet
)

router = DefaultRouter()
router.register(r'hero', HeroSlideViewSet, basename='hero')
router.register(r'features', HomeFeatureViewSet, basename='features')

urlpatterns = [
    path('', include(router.urls)),
    path('about/', HomeAboutViewSet.as_view({'get': 'list'}), name='about'),
    path('cta/', HomeCTAViewSet.as_view({'get': 'list'}), name='cta'),
]
