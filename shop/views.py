from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def shop(request):
    """A view to show all products, including sorting and search queries"""
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    """ Mapping of sorting keys to model fields """
    sort_mapping = {
        'name': 'name',
        'price': 'price',
        'rating': 'rating',
    }

    if request.GET:
        """ Handle sorting """
        sort = request.GET.get('sort', 'name') # Default sorting by name
        direction = request.GET.get('direction', 'asc')
        
        if sort in sort_mapping:
            sortkey = sort_mapping[sort]
            if direction == 'desc':
                sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        
        """ Handle filtering by brand and gender """
        selected_brand = request.GET.get('brand')
        selected_gender = request.GET.get('gender')
        
        if selected_brand:
            products = products.filter(categories__name__iexact=selected_brand)
        
        if selected_gender:
            products = products.filter(categories__name__iexact=selected_gender)
        
        """ Handle search """
        query = request.GET.get('q')
        if query:
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_brand': selected_brand,
        'current_gender': selected_gender,
        'current_sorting': current_sorting,
    }

    return render(request, 'shop/shop.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'shop/product_page.html', context)
