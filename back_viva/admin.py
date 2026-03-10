from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# ---- Branding básico ----
admin.site.site_header = "Diffiori Café"
admin.site.site_title  = "Diffiori Admin"          # <title> del navegador
admin.site.index_title = _("Gestión de Contenido")

# (opcional) cambia el icono del navegador añadiendo un favicon en
# templates/admin/base_site.html → ver paso 2.
