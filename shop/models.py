from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.friendly_name if self.friendly_name else self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    categories = models.ManyToManyField('Category', related_name='products', blank=True)
    name = models.CharField(max_length=254)
    sku = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = CloudinaryField('image', default='placeholder')
    availability = models.BooleanField(default=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    featured_product = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name