from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import loginUser, uploadFile, keyingscreen_view, save_data, download_view


urlpatterns = [
    path("", loginUser, name="login"),
    path("upload/", uploadFile, name="upload"),
    path("keyingscreen/", keyingscreen_view, name="keyingscreen_view"),
    path("save_data", save_data, name="save_data"),
    path("download", download_view, name="download"),
]
