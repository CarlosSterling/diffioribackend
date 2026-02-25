import os
import django

# Setup Django atmosphere
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_viva.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
password = 'admin123'

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"Password for user '{username}' has been reset to '{password}'.")
except User.DoesNotExist:
    User.objects.create_superuser(username=username, password=password, email='')
    print(f"Superuser '{username}' has been created with password '{password}'.")
