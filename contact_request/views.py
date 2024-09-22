from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm


def contact_request(request):
    # Create an empty form instance
    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                (
                    "Thanks for reaching out! "
                    "We got your message and will be in touch within 24 hours."
                    )
            )
            # Reset the form to clear input fields
            contact_form = ContactForm()

    return render(
        request,
        "contact_request/contact_request.html",
        {
            "contact_form": contact_form,
            },
    )