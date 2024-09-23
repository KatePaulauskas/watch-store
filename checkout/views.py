from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import OrderForm
from .models import Order, OrderLineItem, AddOn
from shop.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from cart.contexts import cart_contents
from delivery_method.models import DeliveryMethod

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Fetch available add-ons
    add_ons = AddOn.objects.all()

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        selected_delivery_method_id = request.POST.get('delivery_method')
        # Use the selected delivery method or fall back to standard if none is selected
        if selected_delivery_method_id:
            selected_delivery_method = get_object_or_404(DeliveryMethod, pk=selected_delivery_method_id)
        else:
            selected_delivery_method = DeliveryMethod.objects.filter(name='Standard: 5-10 days').first()

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
            'delivery_method': selected_delivery_method,
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.delivery_method = selected_delivery_method
            order.save()
            
            # Calculate delivery cost based on the selected or default delivery method
            cart_weight = sum([
                item_data * get_object_or_404(Product, pk=item_id).weight if get_object_or_404(Product, pk=item_id).weight is not None else Decimal('1.00')
                for item_id, item_data in cart.items()
            ])
            
            delivery_cost = round(selected_delivery_method.rate * cart_weight)
            order.delivery_cost = delivery_cost  # Store the calculated delivery cost

            selected_add_ons = request.POST.getlist('add_ons')
            if selected_add_ons:
                add_ons_queryset = AddOn.objects.filter(pk__in=selected_add_ons)
                order.add_ons.set(add_ons_queryset)

            # Create order line items and save the order
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database."
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            # Update order with totals, including add-ons and delivery cost
            order.update_total() 
            
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('thank_you', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:

        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment")
            return redirect(reverse('shop'))
        
        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            payment_method_types=['card'],
            )

        # Attempt to prefill the form with any info the user maintains in their profile
        if request.user.is_authenticated:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            order_form = OrderForm(initial={
                'full_name': profile.user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'town_or_city': profile.default_town_or_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'county': profile.default_county,
            })
        else:
            order_form = OrderForm()
    
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'add_ons': add_ons,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        # Update or create the UserProfile associated with the user
        profile, created = UserProfile.objects.update_or_create(
            user=request.user,
            defaults={
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
        )

        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

    # Prepare email content using templates
    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {'order': order}
    )
    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
    )

    # Send order confirmation email
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )

    # Send order confirmation email
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )

    # Clear the cart session
    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/thank_you.html'
    context = {
        'order': order,
    }

    return render(request, template, context)