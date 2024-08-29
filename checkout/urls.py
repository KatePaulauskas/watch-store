from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('thank_you/<order_number>', views.checkout_success, name='thank_you'),
    path('wh/', webhook, name='webhook'),
]