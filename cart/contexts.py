from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Product
from delivery_method.models import DeliveryMethod

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

    # Calculate cart weight
    cart_weight = Decimal('0.00')
    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        if product.weight is not None:
            product_weight = product.weight
        else:
            product_weight = Decimal('1.00')
        cart_weight += product_weight * quantity

    # Default to standard delivery method
    standard_delivery = DeliveryMethod.objects.filter(name='Standard: 5-10 days').first()
    if standard_delivery:
        delivery = round(standard_delivery.rate * cart_weight)
    else:
        delivery = Decimal(settings.STANDARD_DELIVERY)

    grand_total = total + delivery
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
        'cart_weight': cart_weight,
    }

    return context
