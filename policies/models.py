from django.db import models
from django.contrib.auth.models import User

class Policy(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Policies"
        ordering = ['position']

    def __str__(self):
        return self.title