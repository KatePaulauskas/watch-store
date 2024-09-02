from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Product

def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    # Calculate the total and count products in the cart
    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += product.price * quantity
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    # Determine the delivery charge based on user preference
    if 'priority' in request.GET:
        delivery = Decimal(settings.PRIORITY_DELIVERY)
    else:
        delivery = Decimal(settings.STANDARD_DELIVERY)
    
    grand_total = total + delivery
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context