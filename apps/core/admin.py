from django.contrib import admin
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("question", "question_en", "answer", "answer_en")
    
    fieldsets = (
        ("Pregunta y Respuesta (Español)", {
            "fields": ("question", "answer")
        }),
        ("Pregunta y Respuesta (Inglés)", {
            "fields": ("question_en", "answer_en")
        }),
        ("Configuración", {
            "fields": ("order", "is_active")
        }),
    )
