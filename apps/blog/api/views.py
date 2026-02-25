from rest_framework import viewsets, permissions, filters
from apps.blog.models import BlogPost
from . import serializers


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = serializers.BlogPostSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ("title", "excerpt", "content")
