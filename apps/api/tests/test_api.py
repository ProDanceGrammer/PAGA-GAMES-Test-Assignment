import pytest
from rest_framework import status
from apps.integrations.models import AggregatedContent
from django.utils import timezone


@pytest.mark.django_db
class TestContentAPI:
    def test_list_content_requires_auth(self, api_client):
        response = api_client.get('/api/v1/content/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_content_authenticated(self, authenticated_client, nasa_content, weather_content):
        response = authenticated_client.get('/api/v1/content/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 2

    def test_retrieve_content(self, authenticated_client, nasa_content):
        response = authenticated_client.get(f'/api/v1/content/{nasa_content.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == nasa_content.title
        assert response.data['source'] == 'nasa'

    def test_filter_by_source(self, authenticated_client, nasa_content, weather_content, movie_content):
        # should only return NASA content
        response = authenticated_client.get('/api/v1/content/?source=nasa')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['source'] == 'nasa'

    def test_search_content(self, authenticated_client, nasa_content, weather_content):
        response = authenticated_client.get('/api/v1/content/?search=NASA')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_ordering_content(self, authenticated_client, nasa_content, weather_content):
        response = authenticated_client.get('/api/v1/content/?ordering=-published_date')
        assert response.status_code == status.HTTP_200_OK
        results = response.data['results']
        if len(results) > 1:
            assert results[0]['published_date'] >= results[1]['published_date']

    def test_by_source_endpoint(self, authenticated_client, nasa_content, weather_content):
        response = authenticated_client.get('/api/v1/content/by_source/?source=weather')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['source'] == 'weather'

    def test_by_source_missing_parameter(self, authenticated_client):
        response = authenticated_client.get('/api/v1/content/by_source/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_by_date_range(self, authenticated_client):
        past_date = timezone.now() - timezone.timedelta(days=7)
        future_date = timezone.now() + timezone.timedelta(days=1)

        AggregatedContent.objects.create(
            source='nasa',
            title='Old Content',
            description='Test',
            published_date=past_date,
            raw_data={}
        )

        AggregatedContent.objects.create(
            source='nasa',
            title='New Content',
            description='Test',
            published_date=timezone.now(),
            raw_data={}
        )

        # Format date as YYYY-MM-DD HH:MM:SS for django-filter
        date_str = past_date.strftime('%Y-%m-%d %H:%M:%S')
        response = authenticated_client.get(
            f'/api/v1/content/?published_after={date_str}'
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_pagination(self, authenticated_client):
        # Create 25 items to test pagination
        for i in range(25):
            AggregatedContent.objects.create(
                source='nasa',
                title=f'Pagination Test {i}',
                description='Test',
                published_date=timezone.now(),
                raw_data={}
            )

        response = authenticated_client.get('/api/v1/content/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        # With pagination, should have next link if more than 20 items
        total_count = AggregatedContent.objects.count()
        if total_count > 20:
            assert 'next' in response.data


@pytest.mark.django_db
class TestContentSerialization:
    def test_content_serializer_fields(self, authenticated_client, nasa_content):
        response = authenticated_client.get(f'/api/v1/content/{nasa_content.id}/')
        assert response.status_code == status.HTTP_200_OK

        expected_fields = [
            'id', 'source', 'source_display', 'title', 'description',
            'content_url', 'image_url', 'published_date', 'fetched_at', 'raw_data'
        ]
        for field in expected_fields:
            assert field in response.data

    def test_source_display_field(self, authenticated_client, nasa_content):
        response = authenticated_client.get(f'/api/v1/content/{nasa_content.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['source_display'] == 'NASA APOD'
