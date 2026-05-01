from typing import List, Dict, Any
from django.conf import settings
from django.utils.dateparse import parse_datetime
from .base import BaseAPIService
import logging

logger = logging.getLogger(__name__)


class NASAService(BaseAPIService):
    BASE_URL = 'https://api.nasa.gov/planetary/apod'

    def fetch_data(self) -> List[Dict[str, Any]]:
        params = {
            'api_key': settings.NASA_API_KEY,
            'count': 1,
        }
        raw_data = self.make_request(self.BASE_URL, params)

        if isinstance(raw_data, list):
            return [self.normalize_data(item) for item in raw_data]
        return [self.normalize_data(raw_data)]

    def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        # NASA API sometimes returns date without time, need to handle both formats
        date_str = raw_data.get('date', '')
        published_date = parse_datetime(date_str)
        if not published_date and date_str:
            # fallback for date-only format
            published_date = parse_datetime(f"{date_str}T00:00:00Z")

        return {
            'source': 'nasa',
            'title': raw_data.get('title', ''),
            'description': raw_data.get('explanation', ''),
            'content_url': raw_data.get('hdurl', raw_data.get('url', '')),  # prefer HD version
            'image_url': raw_data.get('url', ''),
            'published_date': published_date,
            'raw_data': raw_data,
        }
