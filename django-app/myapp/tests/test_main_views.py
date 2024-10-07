import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(username='adminuser', password='admin12345')

def test_homepage_view(client):
    url = reverse("homepage")
    response = client.get(url)
    assert response.status_code == 200
    assert "homepage.html" in [t.name for t in response.templates]

def test_homepage_view_authenticated(client, user):
    client.login(username='testuser', password='12345')
    url = reverse("homepage")
    response = client.get(url)
    assert response.status_code == 200
    assert "homepage.html" in [t.name for t in response.templates]

def test_analysis_view_authenticated(client, user):
    client.login(username='testuser', password='12345')
    url = reverse("analysis")
    response = client.get(url)
    assert response.status_code == 200
    assert "analysis.html" in [t.name for t in response.templates]

def test_analysis_view_unauthenticated(client):
    url = reverse("analysis")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith('/login/')

def test_analysis_view_admin(client, admin_user):
    client.login(username='adminuser', password='admin12345')
    url = reverse("analysis")
    response = client.get(url)
    assert response.status_code == 200
    assert "analysis.html" in [t.name for t in response.templates]

def test_create_user(client):
    url = reverse("create_user")
    response = client.post(url, {
        'username': 'newuser',
        'password1': 'newpassword123',
        'password2': 'newpassword123'
    })
    assert response.status_code == 302
    assert User.objects.filter(username='newuser').exists()

def test_login_redirect(client, user):
    url = reverse("login")
    response = client.post(url, {
        'username': 'testuser',
        'password': '12345'
    })
    assert response.status_code == 302
    assert response.url == reverse("homepage")
