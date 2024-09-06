from django.urls import path
from . import views
from .views import cancel_action

urlpatterns = [
    path('', views.shop, name='shop'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('cancel_action/', cancel_action, name='cancel_action'),
]