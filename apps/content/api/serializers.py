from rest_framework import serializers
from ..models import HeroSlide, HomeAbout, HomeFeature, HomeCTA

class HeroSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSlide
        fields = "__all__"

class HomeAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeAbout
        fields = "__all__"

class HomeFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeFeature
        fields = "__all__"

class HomeCTASerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeCTA
        fields = "__all__"
