from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages

from shop.models import Product


def view_cart(request):
    """ A view to render the cart contents page """

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """Add a quantity of the specified product to the shopping cart"""
    
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in cart:
        cart[item_id] += quantity
        messages.success(request, f'{product.name} quantity was updated to {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(request, f'{product.name} was added to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)

def adjust_cart(request, item_id):
    """Adjust product quantity"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'{product.name} quantity was updated to {cart[item_id]}')
    else:
        cart.pop(item_id)
        messages.success(request, f'{product.name} was removed from the cart!')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))

def remove_from_cart(request, item_id):
    """Remove item from the shopping cart"""
    
    try:
        product = get_object_or_404(Product, pk=item_id)
        cart = request.session.get('cart', {})

        cart.pop(item_id)
        messages.success(request, f'{product.name} was removed from the cart!')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)