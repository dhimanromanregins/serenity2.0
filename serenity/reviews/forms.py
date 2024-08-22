from django import forms
from .models import Review, Feedback

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


from django import forms
from .models import Feedback  # Adjust the import according to your project structure

from django import forms
from .models import Feedback  # Adjust the import according to your project structure

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 20, 'placeholder': 'Enter your feedback here...'}),
        }

