from django import forms
from django.core import validators
from .models import Policy
import re

class PolicyForm(forms.ModelForm):

    title = forms.CharField(
        error_messages={'required': 'Please enter the policy title.'},
        min_length=5,
        max_length=150,
        help_text="Title should be between 5 and 60 characters."
    )

    content = forms.CharField(
        error_messages={'required': 'Please enter the policy content.'},
        min_length=100,
        max_length=7000,
        help_text="Policy content should be between 100 and 7000 characters.",
        widget=forms.Textarea(attrs={'rows': 10}),
        validators=[
            validators.RegexValidator(
                regex=r'.*[a-zA-Z]+.*',
                message="Policy content must contain letters.",
                code='invalid_content'
            ),
        ]
    )


    class Meta:
        model = Policy
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data.get('title').strip()

        if len(title) < 5:
            raise forms.ValidationError(
                "Policy title must be at least 5 characters long."
            )

        if len(title) > 150:
            raise forms.ValidationError(
                "Policy title cannot exceed 150 characters."
            )

        if not re.search(r'[a-zA-Z]', title):
            raise forms.ValidationError("Policy title must contain letters.")

        if title.isdigit():
            raise forms.ValidationError(
                "Policy title cannot consist of numbers only."
            )

        invalid_chars = set('<>!@#$%^&*()_+[]{}|;:\'",.?/~`\\=')

        if any(char in invalid_chars for char in title):
            raise forms.ValidationError(
                "Policy title contains invalid characters. "
                "Please avoid using special symbols."
            )

        return title

