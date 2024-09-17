from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    category_1 = forms.ModelChoiceField(queryset=Category.objects.all(), label=" Category 1")
    category_2 = forms.ModelChoiceField(queryset=Category.objects.all(), label="Category 2")
    # Add the weight label with the unit
    weight = forms.DecimalField(label="Weight (kg)")

    class Meta:
        model = Product
        exclude = ('categories',)

    def save(self, commit=True):
        # Override save method to handle the many-to-many relationship
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.categories.set([self.cleaned_data['category_1'], self.cleaned_data['category_2']])
        return instance
