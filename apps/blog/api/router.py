from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.BlogPostViewSet, basename="post")
urlpatterns = router.urls
