import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.fixture
def client():
    return Client()

def test_homepeage_view(client):
    url = reverse("homepage")
    response = client.get(url)
    assert response.status_code == 200
    assert "homepage.html" in [t.name for t in response.templates]
