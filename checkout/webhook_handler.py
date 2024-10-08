from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from shop.models import Product
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Send the user a confirmation email
        """
        try:
            cust_email = order.email
            subject = render_to_string(
                'checkout/confirmation_emails/confirmation_email_subject.txt',
                {'order': order})
            body = render_to_string(
                'checkout/confirmation_emails/confirmation_email_body.txt',
                {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email]
            )
            print(f"Confirmation email sent to {cust_email}")
        except Exception as e:
            print(f"Error sending confirmation email: {e}")

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.get('save_info', 'false').lower() == 'true'

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.get('username', 'AnonymousUser')

        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    address = shipping_details.address
                    profile.default_phone_number = shipping_details.get(
                        'phone',
                        profile.default_phone_number
                    )
                    profile.default_country = address.get(
                        'country',
                        profile.default_country
                    )
                    profile.default_postcode = address.get(
                        'postal_code',
                        profile.default_postcode
                    )
                    profile.default_town_or_city = address.get(
                        'city',
                        profile.default_town_or_city
                    )
                    profile.default_street_address1 = address.get(
                        'line1',
                        profile.default_street_address1
                    )
                    profile.default_street_address2 = address.get(
                        'line2',
                        profile.default_street_address2
                    )
                    profile.default_county = address.get(
                        'state',
                        profile.default_county
                    )
                    profile.save()
            except UserProfile.DoesNotExist:
                pass

        # Check if the order already exists
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            # If the order exists, send a confirmation email
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: \
                Verified order already in database',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()  # Rollback if there's an error
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500
                )

        # Send confirmation email after the order is created
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: \
            Created order in webhook',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
