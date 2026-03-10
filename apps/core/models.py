from django.db import models

class FAQ(models.Model):
    question    = models.CharField("Pregunta (Español)", max_length=160)
    question_en = models.CharField("Pregunta (Inglés)", max_length=160, blank=True)
    answer      = models.TextField("Respuesta (Español)")
    answer_en   = models.TextField("Respuesta (Inglés)", blank=True)
    order       = models.PositiveIntegerField("Orden", default=0)
    is_active   = models.BooleanField("Activo", default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question
