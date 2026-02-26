from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Campos base de AbstractUser: username, password, email, first_name, last_name, etc.
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username
