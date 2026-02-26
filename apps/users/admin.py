from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    
    # Agregar 'phone' al panel de edición del admin de Django
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('phone',)}),
    )
