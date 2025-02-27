from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import register_view

urlpatterns = [
    path('register/', register_view, name="register/"),
]
