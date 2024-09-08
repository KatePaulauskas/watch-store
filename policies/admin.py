from django.contrib import admin
from .models import Policy

class PolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at',)

admin.site.register(Policy, PolicyAdmin)
