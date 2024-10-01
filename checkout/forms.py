from django import forms
from .models import Order
from delivery_method.models import DeliveryMethod


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number', 'street_address1',
                  'street_address2', 'town_or_city', 'postcode', 'country',
                  'county', 'delivery_method')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Region',
        }

        self.fields['delivery_method'] = forms.ModelChoiceField(
            queryset=DeliveryMethod.objects.all(),
            label='Delivery Method',
            widget=forms.RadioSelect(),
            empty_label=None,
        )

        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Set placeholders for fields and add accessibility labels
        for field in self.fields:
            if field != 'country' and field != 'delivery_method':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

        # Add aria-label for the 'country' field for screen readers
        self.fields['country'].widget.attrs.update({
            'class': 'stripe-style-input form-select',
            'aria-label': 'Country'
        })

        # Add aria-label for 'delivery_method' field for screen readers
        self.fields['delivery_method'].widget.attrs.update({
            'aria-label': 'Delivery Method'
        })

    def clean_full_name(self):
        """
        Custom validation for the 'full_name' field
        """
        full_name = self.cleaned_data.get('full_name')

        # Check that full name has both first and last names
        if len(full_name.split()) < 2:
            raise forms.ValidationError(
                'Please enter your full name (first and last).'
            )

        # Check that full name contains only letters, apostrophes, and dashes
        if not re.match(r"^[\p{L}'-\s]+$", full_name, re.UNICODE):
            raise forms.ValidationError(
                "Only letters, apostrophes, and dashes are allowed."
            )

        return full_name

    def clean_email(self):
        """
        Custom validation for email
        """
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise forms.ValidationError(
                "Email must end with '@example.com'."
            )
        return email

    def clean_phone_number(self):
        """
        Custom validation for phone number
        """
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError(
                "Phone number must contain only digits."
            )
        if len(phone_number) != 10:
            raise forms.ValidationError(
                "Phone number must be 10 digits long."
            )
        return phone_number

    def clean(self):
        """
        Custom Validation for Street Address 1 and Postal code
        """
        cleaned_data = super().clean()
        street_address1 = cleaned_data.get('street_address1')
        postcode = cleaned_data.get('postcode')

        if not street_address1:
            raise forms.ValidationError("Street Address 1 is required.")
        if not postcode:
            raise forms.ValidationError("Postal code is required.")
