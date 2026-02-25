from rest_framework import serializers
from apps.blog.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    def get_cover_image(self, obj):
        request = self.context.get("request")
        if request and obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

    class Meta:
        model = BlogPost
        fields = "__all__"
