from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

def shop(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    selected_brand = request.GET.get('brand', None)
    selected_gender = request.GET.get('gender', None)

    if selected_brand:
        products = products.filter(categories__name__iexact=selected_brand)
        
    if selected_gender:
        products = products.filter(categories__name__iexact=selected_gender)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('shop'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_brand': selected_brand,
        'current_gender': selected_gender,
    }

    return render(request, 'shop/shop.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'shop/product_page.html', context)
