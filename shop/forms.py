from django import forms
from .models import Product, Category
import re


class ProductForm(forms.ModelForm):

    name = forms.CharField(
        error_messages={'required': 'Please enter the product name.'},
        max_length=255,
        help_text="Name should be between 3 and 255 characters."
    )
    
    # Display friendly names for categories dropdowns
    category_1 = forms.ModelChoiceField(
        queryset=Category.objects.exclude(name__in=['women', 'men']).order_by('name'),
        label="Brand Category",
        widget=forms.Select,
        error_messages={'required': 'Please select brand category.'},
    )

    category_2 = forms.ModelChoiceField(
        queryset=Category.objects.filter(name__in=['women', 'men']).order_by('name'),
        label="Gender Category",
        widget=forms.Select,
        error_messages={'required': 'Please select gender category.'},
    )

    # Ensure price is greater than zero
    price = forms.DecimalField(
        label="Price, €",
        min_value=1,
        max_digits=8,
        decimal_places=2,
    )

    # Ensure weight is between 0.05 and 1.5 kgs
    weight = forms.DecimalField(
        label="Weight (kg)",
        min_value=0.05,
        max_value=1.5,
        max_digits=3,
        decimal_places=2,
    )

    # Ensure rating is greater than zero and up to 5
    rating = forms.DecimalField(
        label="Rating",
        min_value=1,
        max_value=5,
        max_digits=2,
        decimal_places=1,
        help_text="Rating must be between 1 and 5."
    )

    # Image field (optional)
    image = forms.ImageField(
        label="Product Image",
        required=False,
    )

    class Meta:
        model = Product
        exclude = ('categories',)

    def clean_name(self):
        # Validate product name
        name = self.cleaned_data.get('name').strip()

        # Ensure name is not too short
        if len(name) < 3:
            raise forms.ValidationError("Product name must be at least 3 characters long.")

        # Ensure name does not exceed max length (handled by CharField)
        if len(name) > 255:
            raise forms.ValidationError("Product name cannot exceed 255 characters.")
        
        # Ensure name contains at least one letter
        if not re.search(r'[a-zA-Z]', name):
            raise forms.ValidationError("Product name must contain leasts.")

        # Ensure name is not numbers only
        if name.isdigit():
            raise forms.ValidationError("Product name cannot consist of numbers only.")

        # List of characters to exclude
        invalid_chars = set('<>!@#$%^&*()_+[]{}|;:\'",.?/~`\\=')

        # Check for invalid characters in the product name
        if any(char in invalid_chars for char in name):
            raise forms.ValidationError(
                "Product name contains invalid characters. Please avoid using special symbols."
            )
        return name

    def save(self, commit=True):
        # Override save method to handle the many-to-many relationship
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.categories.set([
                self.cleaned_data['category_1'],
                self.cleaned_data['category_2']
            ])
        return instance

