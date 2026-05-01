from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class BaseAPIService(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Django-API-Aggregator/1.0'})

    @abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def normalize_data(self, raw_data: Any) -> Dict[str, Any]:
        pass

    def make_request(self, url: str, params: Dict[str, Any] = None, timeout: int = 10) -> Dict[str, Any]:
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f'API request failed for {url}: {str(e)}')
            raise
