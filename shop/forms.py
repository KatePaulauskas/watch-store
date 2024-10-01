from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    # Display friendly names for categories dropdowns
    category_1 = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'),
        label="Category 1",
        widget=forms.Select
    )

    category_2 = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'),
        label="Category 2",
        widget=forms.Select
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
