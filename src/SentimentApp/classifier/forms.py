from classifier.models import SentimentFeature
from django import forms

class SentimentFeatureForm(forms.ModelForm):
    class Meta: 
        model = SentimentFeature
        fields = ['text']