"""
Celery configuration for Django API Aggregator project.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('config')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'fetch-nasa-daily': {
        'task': 'apps.integrations.tasks.fetch_nasa_data',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
    'fetch-weather-hourly': {
        'task': 'apps.integrations.tasks.fetch_weather_data',
        'schedule': crontab(minute=0),  # Every hour
    },
    'fetch-movies-daily': {
        'task': 'apps.integrations.tasks.fetch_movie_data',
        'schedule': crontab(hour=6, minute=0),  # Daily at 6 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
