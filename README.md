# Django API Aggregator

A full-stack Django application that aggregates content from multiple external APIs (NASA, OpenWeather, TMDB) and provides a unified REST API with JWT authentication, background task processing, caching, and a responsive web interface.

## Features

- **User Authentication**: JWT-based authentication with custom User model
- **API Integration**: Fetches data from NASA APOD, OpenWeather, and TMDB APIs
- **REST API**: Full-featured REST API with filtering, search, and pagination
- **Background Tasks**: Celery-based periodic tasks for data fetching
- **Caching**: Redis-based caching for improved performance
- **Web Interface**: Responsive Bootstrap-based dashboard with data visualization
- **API Documentation**: Interactive Swagger/OpenAPI documentation

## Tech Stack

- **Backend**: Django 5.0+, Django REST Framework 3.14+
- **Database**: PostgreSQL 15+
- **Cache/Broker**: Redis 7+
- **Task Queue**: Celery 5.3+ with Beat scheduler
- **Frontend**: Bootstrap 5, Chart.js
- **Authentication**: JWT (djangorestframework-simplejwt)

## Project Structure

```
.
├── apps/
│   ├── users/          # User authentication and management
│   ├── integrations/   # External API services and models
│   └── api/            # REST API endpoints
├── config/
│   ├── settings/       # Settings (base, development, production)
│   ├── celery.py       # Celery configuration
│   ├── urls.py         # Main URL configuration
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
├── frontend/
│   ├── templates/      # HTML templates
│   ├── static/         # Static files
│   ├── views.py        # Frontend views
│   └── urls.py         # Frontend URLs
├── logs/               # Application logs
├── requirements/       # Python dependencies
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env                # Environment variables
├── docker-compose.yml  # Docker services (PostgreSQL, Redis)
├── Dockerfile          # Docker image configuration
└── manage.py           # Django management script
```

## Setup Instructions

### Prerequisites

- Python 3.14+
- PostgreSQL 15+
- Redis 7+
- Docker (optional, for containerized services)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Test-Assignment-Project
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows
# source .venv/bin/activate    # On Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements/development.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Required environment variables:
- `SECRET_KEY`: Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: PostgreSQL credentials
- `REDIS_URL`: Redis connection URL
- `NASA_API_KEY`: NASA API key (get from https://api.nasa.gov/)
- `OPENWEATHER_API_KEY`: OpenWeather API key (get from https://openweathermap.org/api)
- `TMDB_API_KEY`: TMDB API key (get from https://www.themoviedb.org/settings/api)

### 5. Start Services with Docker

```bash
docker-compose up -d
```

This starts PostgreSQL and Redis containers.

**Note**: PostgreSQL is configured to run on port **5433** (instead of the default 5432) to avoid conflicts with local PostgreSQL installations. If you need to change this, update both `docker-compose.yml` and the `DB_PORT` in your `.env` file.

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Start Development Server

```bash
python manage.py runserver
```

### 9. Start Celery Worker (in separate terminal)

```bash
# On Linux/Mac
celery -A config worker -l info

# On Windows (use solo pool)
celery -A config worker -l info --pool=solo
```

**Note**: Windows requires the `--pool=solo` flag due to limitations with the default prefork pool.

### 10. Start Celery Beat (in separate terminal)

```bash
celery -A config beat -l info
```

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `POST /api/auth/change-password/` - Change password

### Content API

- `GET /api/v1/content/` - List all aggregated content
- `GET /api/v1/content/{id}/` - Get specific content
- `GET /api/v1/content/by_source/?source=nasa` - Filter by source

Query parameters:
- `source`: Filter by source (nasa, weather, movie)
- `search`: Search in title and description
- `published_after`: Filter by published date (>=)
- `published_before`: Filter by published date (<=)
- `ordering`: Order by field (published_date, fetched_at)
- `page`: Page number for pagination

### Documentation

- `GET /api/docs/` - Swagger UI
- `GET /api/schema/` - OpenAPI schema

## Web Interface

- `/` - Home page
- `/login/` - Login page
- `/register/` - Registration page
- `/dashboard/` - Content dashboard (requires authentication)
- `/admin/` - Django admin interface

## Background Tasks

Celery Beat schedules the following periodic tasks:

- **NASA Data**: Fetched daily at midnight
- **Weather Data**: Fetched hourly
- **Movie Data**: Fetched daily at 6 AM

## Testing

Run tests with pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=apps --cov-report=html
```

## Code Quality

Format code with Black:

```bash
black .
```

Sort imports with isort:

```bash
isort .
```

Check code style with flake8:

```bash
flake8
```

Type checking with mypy:

```bash
mypy apps/
```

## Deployment

### Production Settings

1. Set `DEBUG=False` in production settings
2. Configure `ALLOWED_HOSTS`
3. Use strong `SECRET_KEY`
4. Enable HTTPS with proper SSL certificates
5. Configure static files serving
6. Set up proper logging and monitoring

### Docker Deployment

Build and run with Docker:

```bash
docker build -t django-aggregator .
docker run -p 8000:8000 django-aggregator
```

## Troubleshooting

### PostgreSQL Connection Issues

**Problem**: `password authentication failed for user "postgres"` or connection refused on port 5432

**Solution**: 
- Check if you have a local PostgreSQL service running that's using port 5432
- On Windows: Check Task Manager for `postgres.exe` processes
- The project uses port 5433 by default to avoid conflicts
- Verify `DB_PORT=5433` in your `.env` file matches the port in `docker-compose.yml`

**Commands to check**:
```bash
# Check what's using port 5432
netstat -ano | grep :5432

# Verify Docker container is running
docker ps | grep django_aggregator_db

# Check PostgreSQL logs
docker logs django_aggregator_db
```

### Redis Cache Configuration Error

**Problem**: `TypeError: AbstractConnection.__init__() got an unexpected keyword argument 'CLIENT_CLASS'`

**Solution**: 
- This is a compatibility issue between Django's Redis cache backend and newer redis-py versions
- The `CLIENT_CLASS` option has been removed from `config/settings/base.py`
- If you encounter this, ensure your `CACHES` configuration doesn't include the `CLIENT_CLASS` option

### Celery Worker Fails on Windows

**Problem**: `ValueError: not enough values to unpack (expected 3, got 0)` when running Celery worker

**Solution**: 
- Windows doesn't support the default prefork pool
- Use the solo pool instead: `celery -A config worker -l info --pool=solo`
- This is documented in the setup instructions

### API Returns Empty Results Despite Data in Database

**Problem**: API endpoint returns empty results even though data exists in the database

**Solution**: 
- The API uses 15-minute caching
- Clear the Redis cache: `docker exec django_aggregator_redis redis-cli FLUSHALL`
- Or wait for the cache to expire (15 minutes)

### External API Tasks Failing

**Problem**: Weather or Movie tasks fail with 401 Unauthorized errors

**Solution**: 
- These APIs require valid API keys
- Update your `.env` file with real API keys:
  - `OPENWEATHER_API_KEY` - Get from https://openweathermap.org/api
  - `TMDB_API_KEY` - Get from https://www.themoviedb.org/settings/api
- NASA API works with the default `DEMO_KEY` but has rate limits

### Docker Containers Won't Start

**Problem**: Docker containers fail to start or show unhealthy status

**Solution**: 
```bash
# Stop all containers
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Restart services
docker-compose up -d

# Check container logs
docker-compose logs -f
```

### JWT Token Expired

**Problem**: API returns "Token is invalid or expired"

**Solution**: 
- Access tokens expire after 1 hour
- Use the refresh token to get a new access token:
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```
- Or login again to get new tokens

### Migrations Fail

**Problem**: `python manage.py migrate` fails with database errors

**Solution**: 
- Ensure PostgreSQL container is running: `docker ps`
- Check database connection settings in `.env`
- Verify you can connect: `docker exec django_aggregator_db psql -U postgres -d django_aggregator -c "SELECT 1;"`
- If all else fails, reset the database:
```bash
docker-compose down -v
docker-compose up -d
sleep 10
python manage.py migrate
```

### Django Admin AttributeError with Python 3.14

**Problem**: Admin interface shows `AttributeError: 'super' object has no attribute 'dicts'` when accessing any admin page

**Solution**: 
This is a compatibility issue between Python 3.14.0 (very new release) and Django 5.0.14. Django hasn't been fully updated for Python 3.14 yet.

**Option 1: Downgrade to Python 3.13 (Recommended)**
```bash
# Install Python 3.13 from python.org
# Create new virtual environment with Python 3.13
python3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements/development.txt
```

**Option 2: Upgrade to Django 5.1+ (if available)**
```bash
pip install --upgrade django
```

**Option 3: Use API instead of Admin**
- The REST API works fine with Python 3.14
- Use Swagger UI at `http://localhost:8000/api/docs/` instead
- Or use Django shell: `python manage.py shell`

**Workaround (Temporary):**
Access data via Django shell:
```bash
python manage.py shell
>>> from apps.integrations.models import AggregatedContent
>>> AggregatedContent.objects.all()
>>> AggregatedContent.objects.filter(source='nasa')
```

## License

This project is created as a technical assignment.

## Author

YVV - 2026
