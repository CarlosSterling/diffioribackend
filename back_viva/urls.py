from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/password-reset/", auth_views.PasswordResetView.as_view(), name="admin_password_reset"),
    path("admin/password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("admin/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("admin/reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

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

# Branding del admin (fallback si Jazzmin no carga)
admin.site.site_header = "Diffiori Café"
admin.site.site_title = "Diffiori Admin"
admin.site.index_title = "Gestión de Contenido"

# Servir media y static en DEBUG
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
