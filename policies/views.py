from django.shortcuts import render
from .models import Policy

def policies_display(request):
    policies = Policy.objects.all()
    return render(request, 'policies/policies.html', {'policies': policies})
