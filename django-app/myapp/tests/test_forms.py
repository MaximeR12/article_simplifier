import pytest
from main.forms import TextAnalysisForm

@pytest.mark.parametrize(
    "input_text,output_language,validity",
    [
        ("Test input", "English", True),
        ("", "English", False),
        ("Test input", "", False),
    ],
)
def test_text_analysis_form(input_text, output_language, validity):
    form = TextAnalysisForm(data={
        'input_text': input_text,
        'output_language': output_language
    })
    assert form.is_valid() == validity
