from django.shortcuts import (
    render, redirect, reverse, get_object_or_404
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    filters_applied = False  # Track if filters are applied
    reset_filters = False  # Initialize reset_filters
    brand_friendly_name = None
    gender_friendly_name = None

    if 'reset' in request.GET:
        messages.info(request, 'Filters have been reset')
        return redirect('shop')

    sort_mapping = {
        'name': 'name',
        'price': 'price',
        'rating': 'rating',
    }

    if request.GET:
        # Handle sorting
        sort = request.GET.get('sort', None)
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
            brand_category = Category.objects.filter(
                name__iexact=selected_brand
            ).first()
            if brand_category:
                brand_friendly_name = brand_category.get_friendly_name()
                products = products.filter(
                    categories__name__iexact=selected_brand
                )

        if selected_gender:
            gender_category = Category.objects.filter(
                name__iexact=selected_gender
            ).first()
            if gender_category:
                gender_friendly_name = gender_category.get_friendly_name()
                products = products.filter(
                    categories__name__iexact=selected_gender
                )

        # Handle search
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!"
                )
                return redirect(reverse('shop'))

            queries = (
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            products = products.filter(queries)

    current_sorting = (
        f'{sort}_{direction}' if sort else None
    )

    context = {
        'products': products,
        'search_term': query,
        'current_brand': selected_brand,
        'current_gender': selected_gender,
        'brand_friendly_name': brand_friendly_name,
        'gender_friendly_name': gender_friendly_name,
        'current_sorting': current_sorting,
        'sort': sort,
        'direction': direction,
        'reset_filters': reset_filters,
    }

    return render(request, 'shop/shop.html', context)


def product_page(request, product_id):
    """ A view to show individual product pages """
    product = get_object_or_404(Product, pk=product_id)

    context = {'product': product}

    return render(request, 'shop/product_page.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(
            request, 'Only store owner has access to this page.'
        )
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully!')
            return redirect(reverse('product_page', args=[product.id]))
        else:
            messages.error(
                request,
                'There was a problem adding your product, '
                'ensure the form is valid.'
            )
    else:
        form = ProductForm()

    template = 'shop/add_product.html'
    context = {'form': form}

    return render(request, template, context)


@login_required
def manage_products(request):
    """A view to show all products for managing"""
    if not request.user.is_superuser:
        messages.error(
            request, 'Only store owner has access to this page.'
        )
        return redirect(reverse('home'))

    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'shop/manage_products.html', context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(
            request, 'Only store owner has access to this page.'
        )
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    # Retrieve the brand category
    brand_category = product.categories.filter(
        id__in=Category.objects.exclude(name__in=['women', 'men']).values_list('id', flat=True)
    ).first()

    # Retrieve the gender category
    gender_category = product.categories.filter(
        name__in=['women', 'men']
    ).first()

    initial_data = {
        'category_1': brand_category,
        'category_2': gender_category,
    }

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect(reverse('product_page', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product. '
                'Please ensure the form is valid.'
            )
    else:
        form = ProductForm(instance=product, initial=initial_data)

    template = 'shop/edit_product.html'
    context = {'form': form, 'product': product}

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(
            request, 'Only store owner has access to this action.'
        )
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')

    return redirect(reverse('shop'))


@login_required
def cancel_action(request):
    """ Cancel delete action on the shop page """
    messages.add_message(
        request, messages.INFO,
        "Action cancelled. No changes were made."
    )

    return redirect('shop')


@login_required
def cancel_action_manage_products(request):
    """Cancel the action and redirect to the manage products page."""
    messages.add_message(
        request, messages.INFO,
        "Action was canceled. No changes were made."
    )

    return redirect('manage_products')


@login_required
def cancel_action_product_page(request, product_id):
    """ Cancel delete action on the product page """
    product = get_object_or_404(Product, pk=product_id)
    messages.add_message(
        request, messages.INFO,
        "Action cancelled. No changes were made."
    )

    return redirect(reverse('product_page', args=[product.id]))
