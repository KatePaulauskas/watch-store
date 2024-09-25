from django.urls import path
from . import views
from .views import cancel_action_home

urlpatterns = [
    path('', views.index, name='home'),
    path('delete_product/<int:product_id>/', views.delete_product_home, name='delete_product_home'),
    path('cancel_action_home/', cancel_action_home, name='cancel_action_home'),
]