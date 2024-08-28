from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('thank_you/<order_number>', views.checkout_success, name='thank_you'),
]