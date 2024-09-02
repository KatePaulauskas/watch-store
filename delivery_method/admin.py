from django.contrib import admin
from .models import DeliveryMethod


class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate',)

admin.site.register(DeliveryMethod, DeliveryMethodAdmin)