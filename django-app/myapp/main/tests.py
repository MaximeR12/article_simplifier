from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Analysis
from .forms import TextAnalysisForm

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.analysis = Analysis.objects.create(
            user=self.user,
            input_text='Test input',
            output_text='Test output',
            output_language='English'
        )

    def test_analysis_creation(self):
        self.assertTrue(isinstance(self.analysis, Analysis))
        self.assertEqual(self.analysis.__str__(), f"Analysis by {self.user.username} on {self.analysis.timestamp}")

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_analysis_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('analysis'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analysis.html')

    def test_analysis_view_unauthenticated(self):
        response = self.client.get(reverse('analysis'))
        self.assertRedirects(response, '/login/?next=/analysis/')

class FormTests(TestCase):
    def test_text_analysis_form_valid(self):
        form_data = {
            'input_text': 'Test input',
            'output_language': 'English'
        }
        form = TextAnalysisForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_text_analysis_form_invalid(self):
        form_data = {
            'input_text': '',
            'output_language': 'English'
        }
        form = TextAnalysisForm(data=form_data)
        self.assertFalse(form.is_valid())
