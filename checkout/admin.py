from django.contrib import admin
from .models import Order, OrderLineItem, AddOn

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'add_ons_cost',
                       'order_total', 'grand_total',
                       'original_cart', 'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_method',
              'add_ons', 'add_ons_cost', 'delivery_cost',
              'order_total', 'grand_total', 'original_cart',
              'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'add_ons_cost', 'display_add_ons', 'delivery_cost',
                    'grand_total')

    ordering = ('-date',)

    def display_add_ons(self, obj):
        return ", ".join([add_on.name for add_on in obj.add_ons.all()])
    display_add_ons.short_description = 'Add-Ons'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Recalculate the add_ons_cost and grand_total when add-ons are updated
        form.instance.update_total()

class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)

admin.site.register(Order, OrderAdmin)
admin.site.register(AddOn, AddOnAdmin)