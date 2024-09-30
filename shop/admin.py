from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'availability', 'rating',
        'display_categories', 'featured_product',
    )
    list_filter = ('categories', 'price', 'rating',)
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)
    ordering = ('sku',)

    def display_categories(self, obj):
        """Returns a comma-separated list of categories for the product"""
        return ", ".join([
            category.name for category in obj.categories.all()
        ])

    display_categories.short_description = 'Categories'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
