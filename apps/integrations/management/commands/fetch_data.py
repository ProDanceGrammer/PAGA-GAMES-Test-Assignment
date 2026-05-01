from django.core.management.base import BaseCommand
from apps.integrations.tasks import fetch_nasa_data, fetch_weather_data, fetch_movie_data


class Command(BaseCommand):
    help = 'Manually fetch data from all external APIs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            help='Fetch from specific source: nasa, weather, or movie',
        )

    def handle(self, *args, **options):
        source = options.get('source')

        if source == 'nasa':
            self.stdout.write('Fetching NASA data...')
            result = fetch_nasa_data()
            self.stdout.write(self.style.SUCCESS(result))
        elif source == 'weather':
            self.stdout.write('Fetching weather data...')
            result = fetch_weather_data()
            self.stdout.write(self.style.SUCCESS(result))
        elif source == 'movie':
            self.stdout.write('Fetching movie data...')
            result = fetch_movie_data()
            self.stdout.write(self.style.SUCCESS(result))
        else:
            # fetch all if no source specified
            self.stdout.write('Fetching data from all sources...')

            self.stdout.write('- NASA...')
            nasa_result = fetch_nasa_data()
            self.stdout.write(self.style.SUCCESS(f'  {nasa_result}'))

            self.stdout.write('- Weather...')
            weather_result = fetch_weather_data()
            self.stdout.write(self.style.SUCCESS(f'  {weather_result}'))

            self.stdout.write('- Movies...')
            movie_result = fetch_movie_data()
            self.stdout.write(self.style.SUCCESS(f'  {movie_result}'))

            self.stdout.write(self.style.SUCCESS('\nAll data fetched successfully!'))
