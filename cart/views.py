from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
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

    max_quantity = 10
    current_quantity = cart.get(str(item_id), 0)
    new_quantity = current_quantity + quantity

    if new_quantity > max_quantity:
        # Cap the quantity at max_quantity and inform the user
        cart[str(item_id)] = max_quantity
        messages.warning(
            request,
            f"The maximum amount of {max_quantity} for {product.name} has been added to your cart."
        )
    else:
        # Update the cart with the new quantity
        cart[str(item_id)] = new_quantity
        messages.success(
            request,
            f'{product.name} quantity was updated to {cart[str(item_id)]}'
        )

    request.session['cart'] = cart
    return redirect(redirect_url)


def shop_page_add_to_cart(request, item_id):
    """Add product to the shopping cart from the shop page"""

    product = get_object_or_404(Product, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    max_quantity = 10
    current_quantity = cart.get(str(item_id), 0)
    new_quantity = current_quantity + 1

    if new_quantity > max_quantity:
        # Cap the quantity at max_quantity and inform the user
        cart[str(item_id)] = max_quantity
        messages.warning(
            request,
            f"The maximum amount of {max_quantity} for {product.name} has been added to your cart."
        )
    else:
        # Update the cart with the new quantity
        cart[str(item_id)] = new_quantity
        messages.success(
            request,
            f'{product.name} quantity was updated to {cart[str(item_id)]}'
        )

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Adjust product quantity"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    max_quantity = 10

    if quantity > 0:
        if quantity > max_quantity:
            messages.error(
                request, f"You cannot add more than {max_quantity} items of "
                         f"{product.name}."
            )
        else:
            cart[item_id] = quantity
            messages.success(
                request,
                f'{product.name} quantity was updated to {cart[item_id]}'
            )
            request.session['cart'] = cart
    else:
        cart.pop(item_id, None)
        messages.success(request, f'{product.name} was removed from the cart!')
        request.session['cart'] = cart

    return redirect('view_cart')


def remove_from_cart(request, item_id):
    """Remove item from the shopping cart"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        cart = request.session.get('cart', {})

        cart.pop(item_id, None)
        messages.success(request, f'{product.name} was removed from the cart!')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
