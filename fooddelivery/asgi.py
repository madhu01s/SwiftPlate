"""
ASGI config for fooddelivery project.

It exposes the ASGI callable as a module-level variable named
'application'.

For more information:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application



# =========================
# DJANGO SETTINGS MODULE
# =========================

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'fooddelivery.settings'
)



# =========================
# ASGI APPLICATION
# =========================

application = get_asgi_application()
