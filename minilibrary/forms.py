from django import forms


class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a rating between 1 and 5'
        }),
        label="Rating (1-5)"
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your review here...',
            'rows': 4
        }),
        label="Review Text"
    )
