from celery import shared_task
from django.utils import timezone
from .models import AggregatedContent
from .services import NASAService, WeatherService, MovieService
import logging

logger = logging.getLogger(__name__)


@shared_task
def fetch_nasa_data():
    """Fetch daily NASA APOD data"""
    logger.info('Starting NASA data fetch')
    try:
        service = NASAService()
        data_list = service.fetch_data()

        for data in data_list:
            # use update_or_create to avoid duplicates
            AggregatedContent.objects.update_or_create(
                source=data['source'],
                title=data['title'],
                published_date=data['published_date'],
                defaults=data
            )
        logger.info(f'Successfully fetched {len(data_list)} NASA records')
        return f'Fetched {len(data_list)} NASA records'
    except Exception as e:
        logger.error(f'NASA data fetch failed: {str(e)}')
        raise


@shared_task
def fetch_weather_data():
    """Fetch hourly weather data"""
    logger.info('Starting weather data fetch')
    service = WeatherService()
    data_list = service.fetch_data()

    # weather data changes frequently, just create new records
    for data in data_list:
        AggregatedContent.objects.create(**data)
    logger.info(f'Successfully fetched {len(data_list)} weather records')
    return f'Fetched {len(data_list)} weather records'


@shared_task
def fetch_movie_data():
    """Fetch daily popular movies from TMDB"""
    logger.info('Starting movie data fetch')
    try:
        service = MovieService()
        data_list = service.fetch_data()

        for data in data_list:
            AggregatedContent.objects.update_or_create(
                source=data['source'],
                title=data['title'],
                published_date=data['published_date'],
                defaults=data
            )
        logger.info(f'Successfully fetched {len(data_list)} movie records')
        return f'Fetched {len(data_list)} movie records'
    except KeyError as e:
        logger.error(f'Missing required field in movie data: {str(e)}')
        raise
    except Exception as e:
        logger.error(f'Movie data fetch failed: {str(e)}')
        raise
