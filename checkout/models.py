import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from shop.models import Product
from delivery_method.models import DeliveryMethod
from profiles.models import UserProfile


class AddOn(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.PROTECT, null=True, blank=True)
    delivery_cost = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    add_ons = models.ManyToManyField(AddOn, blank=True, related_name='orders')
    add_ons_cost = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex[:8].upper()

    def get_standard_delivery_method(self):
        """Retrieve the default/standard delivery method."""
        return DeliveryMethod.objects.filter(name='Standard: 5-10 days').first()

    def update_total(self):
        """Update grand total each time a line item is added, accounting for delivery costs and add-ons."""
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or Decimal('0')

        # Calculate the total cost of add-ons applied to each line item based on quantity
        add_ons_cost = Decimal('0')
        for lineitem in self.lineitems.all():
            for add_on in self.add_ons.all():
                add_ons_cost += add_on.price * lineitem.quantity

        self.add_ons_cost = add_ons_cost

        # Fallback to standard delivery method if no delivery method is selected
        if not self.delivery_method:
            self.delivery_method = self.get_standard_delivery_method()

        # Calculate delivery cost based on selected delivery method and cart weight (weight * quantity)
        cart_weight = sum([lineitem.product.weight * lineitem.quantity for lineitem in self.lineitems.all()])
        if self.delivery_method:
            self.delivery_cost = round(self.delivery_method.rate * cart_weight)
        else:
            self.delivery_cost = Decimal(0)  # Default to 0 if no delivery method is available

        # Calculate the grand total (order total + delivery cost + add-ons)
        self.grand_total = self.order_total + self.delivery_cost + self.add_ons_cost
        self.save()

    def save(self, *args, **kwargs):
        """Override the original save method to set the order number if it hasn't been set already."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number



class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """Override the original save method to set the lineitem total and update the order total."""
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
