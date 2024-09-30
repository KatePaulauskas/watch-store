from django.urls import path
from . import views
from .views import (
    cancel_action,
    cancel_action_product_page,
    cancel_action_manage_products
)

urlpatterns = [
    path('', views.shop, name='shop'),
    path('<int:product_id>/', views.product_page, name='product_page'),
    path('add/', views.add_product, name='add_product'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path(
        'edit/<int:product_id>/',
        views.edit_product,
        name='edit_product'
    ),
    path(
        'delete/<int:product_id>/',
        views.delete_product,
        name='delete_product'
    ),
    path('cancel_action/', cancel_action, name='cancel_action'),
    path(
        'product/<int:product_id>/cancel/',
        cancel_action_product_page,
        name='cancel_action_product_page'
    ),
    path(
        'manage_products/cancel/',
        cancel_action_manage_products,
        name='cancel_action_manage_products'
    ),
]
