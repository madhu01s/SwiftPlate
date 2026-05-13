"""
WSGI config for fooddelivery project.

It exposes the WSGI callable as a module-level variable named
'application'.

For more information:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application



# =========================
# DJANGO SETTINGS MODULE
# =========================

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'fooddelivery.settings'
)



# =========================
# WSGI APPLICATION
# =========================

application = get_wsgi_application()
