from django import forms

class TextAnalysisForm(forms.Form):
    input_text = forms.CharField(label='Text to analyse', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write or paste your text to analyse'
    }))

    output_language = forms.CharField(label='Result language', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Chose your wanted language for your result'
    }))
