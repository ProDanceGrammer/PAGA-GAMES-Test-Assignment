import pytest
from django.utils import timezone
from apps.integrations.models import AggregatedContent
from apps.integrations.services import NASAService, WeatherService, MovieService
from unittest.mock import patch, MagicMock


@pytest.mark.django_db
class TestAggregatedContentModel:
    def test_create_content(self):
        content = AggregatedContent.objects.create(
            source='nasa',
            title='Test Content',
            description='Test description',
            content_url='https://example.com',
            image_url='https://example.com/image.jpg',
            published_date=timezone.now(),
            raw_data={'test': 'data'}
        )
        assert content.source == 'nasa'
        assert content.title == 'Test Content'
        assert str(content) == 'NASA APOD: Test Content'

    def test_content_ordering(self, nasa_content, weather_content):
        contents = AggregatedContent.objects.all()
        assert contents[0].published_date >= contents[1].published_date


@pytest.mark.django_db
class TestNASAService:
    @patch('apps.integrations.services.nasa.NASAService.make_request')
    def test_fetch_nasa_data(self, mock_request):
        mock_request.return_value = {
            'title': 'Test NASA Image',
            'explanation': 'Test explanation',
            'url': 'https://example.com/image.jpg',
            'hdurl': 'https://example.com/image_hd.jpg',
            'date': '2026-04-30'
        }

        service = NASAService()
        data = service.fetch_data()

        assert len(data) == 1
        assert data[0]['source'] == 'nasa'
        assert data[0]['title'] == 'Test NASA Image'

    def test_normalize_nasa_data(self):
        raw_data = {
            'title': 'Test NASA Image',
            'explanation': 'Test explanation',
            'url': 'https://example.com/image.jpg',
            'hdurl': 'https://example.com/image_hd.jpg',
            'date': '2026-04-30'
        }

        service = NASAService()
        normalized = service.normalize_data(raw_data)

        assert normalized['source'] == 'nasa'
        assert normalized['title'] == 'Test NASA Image'
        assert normalized['description'] == 'Test explanation'
        assert normalized['content_url'] == 'https://example.com/image_hd.jpg'


@pytest.mark.django_db
class TestWeatherService:
    @patch('apps.integrations.services.weather.WeatherService.make_request')
    def test_fetch_weather_data(self, mock_request):
        mock_request.return_value = {
            'name': 'London',
            'weather': [{'description': 'clear sky', 'icon': '01d'}],
            'main': {
                'temp': 15.5,
                'feels_like': 14.2,
                'humidity': 72,
                'pressure': 1013
            }
        }

        service = WeatherService()
        data = service.fetch_data()

        assert len(data) == 1
        assert data[0]['source'] == 'weather'
        assert 'London' in data[0]['title']

    def test_normalize_weather_data(self):
        raw_data = {
            'name': 'London',
            'weather': [{'description': 'clear sky', 'icon': '01d'}],
            'main': {
                'temp': 15.5,
                'feels_like': 14.2,
                'humidity': 72,
                'pressure': 1013
            }
        }

        service = WeatherService()
        normalized = service.normalize_data(raw_data)

        assert normalized['source'] == 'weather'
        assert 'London' in normalized['title']
        assert '15.5' in normalized['description']


@pytest.mark.django_db
class TestMovieService:
    @patch('apps.integrations.services.movie.MovieService.make_request')
    def test_fetch_movie_data(self, mock_request):
        mock_request.return_value = {
            'results': [
                {
                    'id': 123,
                    'title': 'Test Movie',
                    'overview': 'Test overview',
                    'release_date': '2026-04-30',
                    'poster_path': '/test.jpg'
                }
            ]
        }

        service = MovieService()
        data = service.fetch_data()

        assert len(data) == 1
        assert data[0]['source'] == 'movie'
        assert data[0]['title'] == 'Test Movie'

    def test_normalize_movie_data(self):
        raw_data = {
            'id': 123,
            'title': 'Test Movie',
            'overview': 'Test overview',
            'release_date': '2026-04-30',
            'poster_path': '/test.jpg'
        }

        service = MovieService()
        normalized = service.normalize_data(raw_data)

        assert normalized['source'] == 'movie'
        assert normalized['title'] == 'Test Movie'
        assert normalized['description'] == 'Test overview'
        assert 'themoviedb.org' in normalized['content_url']
