from django.shortcuts import render
from shop.models import Product

def index(request):
    """ A view to return the index page """
    featured_products = Product.objects.filter(featured_product=True, availability=True)  # Only fetch available featured products
    return render(request, 'home/index.html', {'featured_products': featured_products})
