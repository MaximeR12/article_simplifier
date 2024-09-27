from django import forms

class TextAnalysisForm(forms.Form):
    input_text = forms.CharField(label='Article to analyse', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write or paste your article to analyse'
    }))

    output_language = forms.CharField(label='Result language', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose your desired language for the result'
    }))
