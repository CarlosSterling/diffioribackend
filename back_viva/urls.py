from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # ─── Documentación OpenAPI ───
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    # ─── Endpoints por app ───
    path("api/productos/", include("apps.catalog.api.router")),
    path("api/clientes/", include("apps.clients.api.router")),
    path("api/posts/", include("apps.blog.api.router")),
    path("api/faqs/", include("apps.core.api.router")),
    path("api/content/", include("apps.content.urls")),
    path("api/orders/", include("apps.orders.api.router")),
]

# Servir media y static en DEBUG
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
