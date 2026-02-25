from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("categories", views.CategoryViewSet, basename="categoria")
router.register("", views.ProductViewSet, basename="producto")
urlpatterns = router.urls
