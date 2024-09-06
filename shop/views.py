from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm


def shop(request):
    """A view to show all products, including sorting and search queries"""
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    selected_brand = None
    selected_gender = None

    # Mapping of sorting keys to model fields
    sort_mapping = {
        'name': 'name',
        'price': 'price',
        'rating': 'rating',
    }

    if request.GET:
        # Handle sorting
        sort = request.GET.get('sort', 'name') # Default sorting by name
        direction = request.GET.get('direction', 'asc')
        
        if sort in sort_mapping:
            sortkey = sort_mapping[sort]
            if direction == 'desc':
                sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        
        # Handle filtering by brand and gender
        selected_brand = request.GET.get('brand', None)
        selected_gender = request.GET.get('gender', None)
        
        if selected_brand:
            products = products.filter(categories__name__iexact=selected_brand)
        
        if selected_gender:
            products = products.filter(categories__name__iexact=selected_gender)
        
        #Handle search
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('shop'))
            
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


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product is added successfully!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'There was a problem adding your product, ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'shop/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
