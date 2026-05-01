from typing import List, Dict, Any
import logging
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_date
from .base import BaseAPIService

logger = logging.getLogger(__name__)


class MovieService(BaseAPIService):
    BASE_URL = 'https://api.themoviedb.org/3/movie/popular'
    IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

    def fetch_data(self) -> List[Dict[str, Any]]:
        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US',
            'page': 1,
        }
        raw_data = self.make_request(self.BASE_URL, params)
        results = raw_data.get('results', [])[:5]
        return [self.normalize_data(item) for item in results]

    def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        release_date = raw_data.get('release_date', '')
        published_date = parse_date(release_date) if release_date else timezone.now().date()

        poster_path = raw_data.get('poster_path', '')
        image_url = f"{self.IMAGE_BASE_URL}{poster_path}" if poster_path else ''

        return {
            'source': 'movie',
            'title': raw_data.get('title', raw_data.get('original_title', '')),
            'description': raw_data.get('overview', ''),
            'content_url': f"https://www.themoviedb.org/movie/{raw_data.get('id', '')}",
            'image_url': image_url,
            'published_date': timezone.make_aware(timezone.datetime.combine(published_date, timezone.datetime.min.time())),
            'raw_data': raw_data,
        }
