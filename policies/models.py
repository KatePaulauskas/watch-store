from django.db import models
from django.core.validators import MinLengthValidator

class Policy(models.Model):
    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )
    content = models.TextField(
        validators=[MinLengthValidator(100)]
    )
    updated_at = models.DateTimeField(auto_now=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Policies"
        ordering = ['position']

    def __str__(self):
        return self.title
