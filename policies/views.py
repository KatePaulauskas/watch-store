from django.shortcuts import render, reverse, redirect,  get_object_or_404
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
    """ View to edit store policies """
    policy = get_object_or_404(Policy, pk=pk)
    if not request.user.is_superuser:
        messages.error(request, 'Only store owner has access to this page.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = PolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            messages.success(request, f'{policy.title} updated successfully!')
            return redirect('policies')
    else:
        form = PolicyForm(instance=policy)
    
    return render(request, 'policies/edit_policy.html', {'form': form, 'policy': policy})

@login_required
def cancel_editing(request):
    """ Cancel delete action on she shop page """
    messages.add_message(request, messages.INFO,
                         "Action cancelled. No changes were made.")

    return redirect('policies')
