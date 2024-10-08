from django.db import models
from django.db.models import DecimalField

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name