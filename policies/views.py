from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Policy
from .forms import PolicyForm

def policies_display(request):
    policies = Policy.objects.all()
    return render(request, 'policies/policies.html', {'policies': policies})

@login_required
def edit_policy(request, pk):
    policy = get_object_or_404(Policy, pk=pk)
    if request.method == 'POST':
        form = PolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            messages.success(request, f'{policy.title} updated successfully!')
            return redirect('policies')
    else:
        form = PolicyForm(instance=policy)
    
    return render(request, 'policies/edit_policy.html', {'form': form, 'policy': policy})

def cancel_editing(request):
    """ Cancel delete action on she shop page """
    messages.add_message(request, messages.INFO,
                         "Action cancelled. No changes were made.")

    return redirect('policies')
