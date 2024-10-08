from django import forms

class TextAnalysisForm(forms.Form):
    input_text = forms.CharField(
        label='Text to analyze',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Paste or write your text here'
        })
    )

    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('German', 'German'),
        ('French', 'French'),
        ('Italian', 'Italian'),
        ('Portuguese', 'Portuguese'),
        ('Hindi', 'Hindi'),
        ('Spanish', 'Spanish'),
        ('Thai', 'Thai'),
    ]

    output_language = forms.ChoiceField(
        label='Result language',
        choices=LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
