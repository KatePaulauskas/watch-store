from django import forms
from django.core import validators
from .models import Product, Category
import re


class ProductForm(forms.ModelForm):

    name = forms.CharField(
        error_messages={'required': 'Please enter the product name.'},
        min_length=3,
        max_length=60,
        help_text="Name should be between 3 and 60 characters."
    )

    sku = forms.CharField(
        required=False,
        max_length=50,
        help_text="SKU should only contain letters, numbers, and dashes.",
        error_messages={
            'invalid': 'SKU can only contain letters, numbers, and dashes.'
        }
    )

    description = forms.CharField(
        error_messages={'required': 'Please enter the product description.'},
        min_length=100,
        max_length=3000,
        help_text="Description should be between 100 and 3000 characters.",
        widget=forms.Textarea(attrs={'rows': 10}),
        validators=[
            validators.RegexValidator(
                regex=r'.*[a-zA-Z]+.*',
                message="Description must contain letters.",
                code='invalid_description'
            ),
        ]
    )

    category_1 = forms.ModelChoiceField(
        queryset=Category.objects.exclude(name__in=['women', 'men']).order_by(
            'name'
        ),
        label="Brand Category",
        widget=forms.Select,
        error_messages={'required': 'Please select brand category.'},
    )

    category_2 = forms.ModelChoiceField(
        queryset=Category.objects.filter(name__in=['women', 'men']).order_by(
            'name'
        ),
        label="Gender Category",
        widget=forms.Select,
        error_messages={'required': 'Please select gender category.'},
    )

    price = forms.DecimalField(
        label="Price, €",
        min_value=1,
        max_digits=8,
        decimal_places=2,
    )

    weight = forms.DecimalField(
        label="Weight (kg)",
        min_value=0.05,
        max_value=1.5,
        max_digits=3,
        decimal_places=2,
        help_text="Weight must be between 0.05 and 1.5 kgs."
    )

    rating = forms.DecimalField(
        label="Rating",
        min_value=1,
        max_value=5,
        max_digits=2,
        decimal_places=1,
        help_text="Rating must be between 1 and 5."
    )

    image = forms.ImageField(
        label="Product Image",
        required=False,
    )

    class Meta:
        model = Product
        exclude = ('categories',)

    def clean_name(self):
        name = self.cleaned_data.get('name').strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "Product name must be at least 3 characters long."
            )

        if len(name) > 60:
            raise forms.ValidationError(
                "Product name cannot exceed 60 characters."
            )

        if not re.search(r'[a-zA-Z]', name):
            raise forms.ValidationError("Product name must contain letters.")

        if name.isdigit():
            raise forms.ValidationError(
                "Product name cannot consist of numbers only."
            )

        invalid_chars = set('<>!@#$%^&*()_+[]{}|;:\'",.?/~`\\=')

        if any(char in invalid_chars for char in name):
            raise forms.ValidationError(
                "Product name contains invalid characters. "
                "Please avoid using special symbols."
            )

        return name

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')

        if sku and not re.match(r'^[a-zA-Z0-9-]+$', sku):
            raise forms.ValidationError(
                "SKU can only contain letters, numbers, and dashes."
            )
        return sku

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.categories.set([
                self.cleaned_data['category_1'],
                self.cleaned_data['category_2']
            ])
        return instance
