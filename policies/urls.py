from django.urls import path
from . import views

urlpatterns = [
    path('', views.policies_display, name='policies'),
]