import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.integrations.models import AggregatedContent
from django.utils import timezone

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def nasa_content(db):
    return AggregatedContent.objects.create(
        source='nasa',
        title='Test NASA Content',
        description='Test description for NASA',
        content_url='https://example.com/nasa',
        image_url='https://example.com/nasa.jpg',
        published_date=timezone.now(),
        raw_data={'test': 'data'}
    )


@pytest.fixture
def weather_content(db):
    return AggregatedContent.objects.create(
        source='weather',
        title='Weather in London',
        description='Temperature: 15°C',
        content_url='',
        image_url='https://example.com/weather.png',
        published_date=timezone.now(),
        raw_data={'temp': 15}
    )


@pytest.fixture
def movie_content(db):
    return AggregatedContent.objects.create(
        source='movie',
        title='Test Movie',
        description='Test movie description',
        content_url='https://example.com/movie',
        image_url='https://example.com/movie.jpg',
        published_date=timezone.now(),
        raw_data={'id': 123}
    )
