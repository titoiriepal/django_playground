from django import forms
from .models import Review

BAD_WORDS = [
    "fuck",
    "stupid",
    "idiot",
    "dumb",
    "awful",
    "terrible",
    "horrible",
    "worst",
    "sucks",
    "trash",
    "garbage",
    "crap",

]


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


class ReviewForm(forms.ModelForm):

    would_recommend = forms.BooleanField(
        label="Would you recommend this book?",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = Review
        fields = ['rating', 'text', 'would_recommend']

        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a rating between 1 and 5'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review here...',
                'rows': 4
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text:
            for bad_word in BAD_WORDS:
                if bad_word in text.lower():
                    raise forms.ValidationError(
                        "Please avoid using inappropriate "
                        "language in your review."
                    )
        return text

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        text = cleaned_data.get('text')

        if rating and not text:
            raise forms.ValidationError(
                "Please provide a review text when giving a rating.")
        elif text and not rating:
            raise forms.ValidationError(
                "Please provide a rating when writing a review.")
        if rating == 1 and len(text) < 10:
            raise forms.ValidationError(
                "Please provide more details for a 1-star review.")

    def save(self, commit=True):
        review = super().save(commit=False)
        # Agregar lógica adicional aquí si es necesario para would_recommend
        # o cualquier otro campo antes de guardar el review
        if commit:
            review.save()
        return review
