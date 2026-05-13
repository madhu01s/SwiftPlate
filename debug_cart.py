import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fooddelivery.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth.models import User

client = Client()
user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
if created:
    user.set_password('pass')
    user.save()
login_success = client.login(username='testuser', password='pass')
print('login', login_success)
resp = client.get('/cart/')
print('status', resp.status_code)
print(resp.content[:2000].decode('utf-8', 'replace'))
