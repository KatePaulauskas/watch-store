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

def shop_page_add_to_cart(request, item_id):
    """Add product to the shopping cart from the shop page"""
    
    product = get_object_or_404(Product, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    # If the product is already in the cart, increase its quantity by 1
    if str(item_id) in cart:
        cart[str(item_id)] += 1
        messages.success(request, f'{product.name} quantity was updated to {cart[str(item_id)]}')
    else:
        # Add the product to the cart with a default quantity of 1
        cart[str(item_id)] = 1
        messages.success(request, f'{product.name} was added to your cart')

    # Save the updated cart to the session
    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Adjust product quantity"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    # Set the maximum allowed quantity
    max_quantity = 10

    if quantity > 0:
        if quantity > max_quantity:
            messages.error(request, f"You cannot add more than {max_quantity} items of {product.name}.")
        else:
            cart[item_id] = quantity
            messages.success(request, f'{product.name} quantity was updated to {cart[item_id]}')
            request.session['cart'] = cart
    else:
        cart.pop(item_id)
        messages.success(request, f'{product.name} was removed from the cart!')
        request.session['cart'] = cart

    return redirect('view_cart')


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