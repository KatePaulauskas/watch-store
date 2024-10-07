from django import forms
from .models import Order
from delivery_method.models import DeliveryMethod
import re


class OrderForm(forms.ModelForm):

    # Full Name Field
    full_name = forms.CharField(
        min_length=3,
        max_length=60,
    )

    # Street Address 1 Field
    street_address1 = forms.CharField(
        min_length=5,
        max_length=100,
    )

    # Street Address 2 Field (Optional)
    street_address2 = forms.CharField(
        required=False,
        max_length=100,
    )

    # Town or City Field
    town_or_city = forms.CharField(
        min_length=2,
        max_length=60,
    )

    # County Field (Optional)
    county = forms.CharField(
        required=False,
        max_length=60,
    )

    # Postal Code Field
    postcode = forms.CharField(
        min_length=3,
        max_length=10,
    )

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

        # Ensure 'postcode' is mandatory
        self.fields['postcode'].required = True

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
        full_name = self.cleaned_data.get('full_name').strip()

        # Check that full name has at least two words
        if len(full_name.split()) < 2:
            raise forms.ValidationError(
                'Enter your full name (first and last).'
            )

        # Check that full name is between 3 and 60 characters
        if len(full_name) < 3:
            raise forms.ValidationError(
                "Full name must be at least 3 characters."
            )

        if len(full_name) > 60:
            raise forms.ValidationError(
                "Full name cannot exceed 60 characters."
            )

        # Ensure name contains letters and does not contain digits
        if not re.match(r"^[a-zA-Z\s'\-]+$", full_name):
            raise forms.ValidationError(
                "Full name can only contain letters,"
                    "spaces, apostrophes, and dashes."
            )

        # Check for invalid characters
        invalid_chars = set('<>!@#$%^&*()_+[]{}|;:\'",.?/~`\\=')

        if any(char in invalid_chars for char in full_name):
            raise forms.ValidationError(
                "Full name contains invalid characters. "
            )

        return full_name

    def clean_phone_number(self):
        """
        Custom validation for phone number
        """
        phone_number = self.cleaned_data.get('phone_number')

        # Ensure the phone number contains only digits
        if not phone_number.isdigit():
            raise forms.ValidationError(
                "Phone number must contain only digits."
            )

        # Ensure the phone number is between 7 and 15 characters long
        if len(phone_number) < 7 or len(phone_number) > 15:
            raise forms.ValidationError(
                "Phone number must be between 7 and 15 digits."
            )

        return phone_number

    def clean(self):
        """
        Custom validation for address fields.
        """
        cleaned_data = super().clean()

        street_address1 = cleaned_data.get('street_address1')
        street_address2 = cleaned_data.get('street_address2')
        town_or_city = cleaned_data.get('town_or_city')
        county = cleaned_data.get('county')
        postcode = cleaned_data.get('postcode')

        # Regex for validation
        address_regex = r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9\s,.\'-]+$'
        letters_only_regex = r'^[a-zA-Z\s\'-]+$'
        postcode_regex = r'^[a-zA-Z0-9\s-]+$'

        # Validate street address 1 (letters and digits)
        if street_address1:
            if not re.match(address_regex, street_address1):
                self.add_error(
                    'street_address1',
                    "Street Address 1 must contain letters and numbers"
                )
        else:
            self.add_error('street_address1', "Street Address 1 is required.")

        # Validate street address 2 (optional, letters and digits)
        if street_address2 and not re.match(address_regex, street_address2):
            self.add_error(
                'street_address2',
                "Street Address 2 must contain letters and numbers"
            )

        # Validate town or city (letters only)
        if town_or_city:
            if not re.match(letters_only_regex, town_or_city):
                self.add_error(
                    'town_or_city',
                    "Town/City must contain letters."
                )
        else:
            self.add_error('town_or_city', "Town/City is required.")

        # Validate county (optional, letters only)
        if county and not re.match(letters_only_regex, county):
            self.add_error(
                'county',
                "County must contain letters."
            )

        # Validate postal code (letters, digits, spaces, and hyphens)
        if postcode:
            if not re.match(postcode_regex, postcode):
                self.add_error(
                    'postcode',
                    "Postal code contains invalid characters. "
                )
        else:
            self.add_error('postcode', "Postal code is required.")

        return cleaned_data
