from django.contrib import admin
from django.urls import path
from chat.views import home, healthz

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("health/", healthz),
]
