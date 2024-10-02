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
