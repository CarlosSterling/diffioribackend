from rest_framework import serializers
from apps.blog.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    def get_cover_image(self, obj):
        if obj.cover_image:
            return obj.cover_image.url  # URL relativa: /media/blog/...
        return None

    class Meta:
        model = BlogPost
        fields = "__all__"
