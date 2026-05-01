# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial project setup with Django 5.0
- Custom User model with email authentication
- JWT authentication endpoints
- NASA APOD API integration
- OpenWeather API integration
- TMDB movie API integration
- REST API with filtering and search
- Celery background tasks for periodic data fetching
- Redis caching for API responses
- Bootstrap frontend with dashboard
- Chart.js data visualization
- Comprehensive test suite
- API documentation with Swagger
- Docker support

### Changed
- Split settings into base/development/production modules
- Improved data normalization for consistent format

### Fixed
- Date parsing for NASA API responses
- Cache key generation for by_source endpoint

## [0.1.0] - 2026-04-30

### Added
- Initial release
- Basic project structure
- Core functionality implemented
