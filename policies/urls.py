from django.urls import path
from . import views

urlpatterns = [
    path('', views.policies_display, name='policies'),
    path('edit/<int:pk>/', views.edit_policy, name='edit_policy'),
    path('cancel_editing/', views.cancel_editing, name='cancel_editing'),
]