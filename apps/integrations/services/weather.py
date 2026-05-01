import logging
from typing import List, Dict, Any
from django.utils import timezone
from django.conf import settings
from .base import BaseAPIService

logger = logging.getLogger(__name__)


class WeatherService(BaseAPIService):
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

    def fetch_data(self) -> List[Dict[str, Any]]:
        params = {
            'appid': settings.OPENWEATHER_API_KEY,
            'q': f"{settings.WEATHER_CITY},{settings.WEATHER_COUNTRY_CODE}",
            'units': 'metric',
        }
        raw_data = self.make_request(self.BASE_URL, params)
        return [self.normalize_data(raw_data)]

    def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        weather = raw_data.get('weather', [{}])[0]
        main = raw_data.get('main', {})

        # TODO: maybe add wind speed and direction to description later
        description = (
            f"Temperature: {main.get('temp', 'N/A')}°C, "
            f"Feels like: {main.get('feels_like', 'N/A')}°C, "
            f"Humidity: {main.get('humidity', 'N/A')}%, "
            f"Pressure: {main.get('pressure', 'N/A')} hPa. "
            f"{weather.get('description', '').capitalize()}"
        )

        return {
            'source': 'weather',
            'title': f"Weather in {raw_data.get('name', 'Unknown')}",
            'description': description,
            'content_url': '',
            'image_url': f"https://openweathermap.org/img/wn/{weather.get('icon', '01d')}@2x.png",
            'published_date': timezone.now(),
            'raw_data': raw_data,
        }
