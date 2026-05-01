from django.db import models
from django.utils import timezone


class AggregatedContent(models.Model):
    SOURCE_CHOICES = [
        ('nasa', 'NASA APOD'),
        ('weather', 'OpenWeather'),
        ('movie', 'TMDB'),
    ]

    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, db_index=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    content_url = models.URLField(max_length=1000, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    published_date = models.DateTimeField(db_index=True)
    fetched_at = models.DateTimeField(default=timezone.now, db_index=True)
    raw_data = models.JSONField()

    class Meta:
        db_table = 'aggregated_content'
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['source', '-published_date']),
            models.Index(fields=['-fetched_at']),
        ]

    def __str__(self):
        return f'{self.get_source_display()}: {self.title}'

