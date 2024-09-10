from backrun_sdk.django import serve
from django.urls import path

urlpatterns = [
    path("backrun/", serve),
]
