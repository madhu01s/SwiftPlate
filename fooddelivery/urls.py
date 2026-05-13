"""
URL configuration for fooddelivery project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap


urlpatterns = [

    # =========================
    # ADMIN PANEL
    # =========================

    path(
        'admin/',
        admin.site.urls
    ),


    # =========================
    # MAIN APP URLS
    # =========================

    path(
        '',
        include('orders.urls')
    ),

]



# =========================
# MEDIA FILES
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )



# =========================
# ADMIN PANEL CUSTOMIZATION
# =========================

admin.site.site_header = "SwiftPlate Admin"

admin.site.site_title = "Food Delivery Admin Panel"

admin.site.index_title = "Welcome to SwiftPlate Dashboard"