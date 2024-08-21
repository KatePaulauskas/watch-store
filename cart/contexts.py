from decimal import Decimal
from django.conf import settings

def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0

    # Calculate the total and count products in the cart (assuming cart_items is populated elsewhere)
    for item in cart_items:
        total += item['price'] * item['quantity']
        product_count += item['quantity']

    # Determine the delivery charge based on user preference
    if 'priority' in request.GET:
        delivery = Decimal(settings.PRIORITY_DELIVERY)
    else:
        delivery = Decimal(settings.STANDARD_DELIVERY)
    
    grand_total = delivery + total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
        }

    return context
   
