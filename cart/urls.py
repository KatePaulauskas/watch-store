from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<int:item_id>', views.add_to_cart, name='add_to_cart'),
    path('shop_page_add_to_cart/<int:item_id>/', views.shop_page_add_to_cart, name='shop_page_add_to_cart'),
    path('adjust/<item_id>/', views.adjust_cart, name='adjust_cart'),
    path('remove/<item_id>/', views.remove_from_cart, name='remove_from_cart'),
]