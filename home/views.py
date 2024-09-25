from django.shortcuts import render, redirect, reverse, get_object_or_404
from shop.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    """ A view to return the index page """
    featured_products = Product.objects.filter(featured_product=True, availability=True)  # Only fetch available featured products
    return render(request, 'home/index.html', {'featured_products': featured_products})

@login_required
def delete_product_home(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Only store owners has access to this action.')
        return redirect(reverse('home'))
        
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')

    return redirect(reverse('home'))

@login_required
def cancel_action_home(request):
    """ Cancel delete action on she shop page """
    messages.add_message(request, messages.INFO,
                         "Action cancelled. No changes were made.")

    return redirect('home')
