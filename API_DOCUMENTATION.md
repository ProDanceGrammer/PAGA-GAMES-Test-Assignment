# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

All API endpoints (except registration and login) require JWT authentication.

### Headers

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Authentication Endpoints

### Register User

**POST** `/auth/register/`

Request:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "password2": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2026-04-30T10:00:00Z"
}
```

### Login

**POST** `/auth/login/`

Request:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

Response (200 OK):
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token

**POST** `/auth/token/refresh/`

Request:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Response (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get User Profile

**GET** `/auth/profile/`

Response (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2026-04-30T10:00:00Z"
}
```

### Update User Profile

**PUT** `/auth/profile/`

Request:
```json
{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

Response (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "date_joined": "2026-04-30T10:00:00Z"
}
```

### Change Password

**POST** `/auth/change-password/`

Request:
```json
{
  "old_password": "oldpassword123",
  "new_password": "newpassword456"
}
```

Response (200 OK):
```json
{
  "detail": "Password updated successfully"
}
```

## Content Endpoints

### List All Content

**GET** `/v1/content/`

Query Parameters:
- `page` (integer): Page number (default: 1)
- `source` (string): Filter by source (nasa, weather, movie)
- `search` (string): Search in title and description
- `published_after` (datetime): Filter by published date (>=)
- `published_before` (datetime): Filter by published date (<=)
- `ordering` (string): Order by field (published_date, -published_date, fetched_at, -fetched_at)

Example Request:
```
GET /v1/content/?source=nasa&page=1&ordering=-published_date
```

Response (200 OK):
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/v1/content/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "source": "nasa",
      "source_display": "NASA APOD",
      "title": "The Horsehead Nebula",
      "description": "One of the most identifiable nebulae in the sky...",
      "content_url": "https://apod.nasa.gov/apod/image/2604/horsehead_hst.jpg",
      "image_url": "https://apod.nasa.gov/apod/image/2604/horsehead_hst.jpg",
      "published_date": "2026-04-30T00:00:00Z",
      "fetched_at": "2026-04-30T10:00:00Z"
    }
  ]
}
```

### Get Content by ID

**GET** `/v1/content/{id}/`

Response (200 OK):
```json
{
  "id": 1,
  "source": "nasa",
  "source_display": "NASA APOD",
  "title": "The Horsehead Nebula",
  "description": "One of the most identifiable nebulae in the sky...",
  "content_url": "https://apod.nasa.gov/apod/image/2604/horsehead_hst.jpg",
  "image_url": "https://apod.nasa.gov/apod/image/2604/horsehead_hst.jpg",
  "published_date": "2026-04-30T00:00:00Z",
  "fetched_at": "2026-04-30T10:00:00Z",
  "raw_data": {
    "date": "2026-04-30",
    "explanation": "One of the most identifiable nebulae...",
    "hdurl": "https://apod.nasa.gov/apod/image/2604/horsehead_hst.jpg",
    "title": "The Horsehead Nebula"
  }
}
```

### Get Content by Source

**GET** `/v1/content/by_source/?source={source}`

Query Parameters:
- `source` (required): Source type (nasa, weather, movie)
- `page` (integer): Page number

Example Request:
```
GET /v1/content/by_source/?source=weather
```

Response (200 OK):
```json
{
  "count": 24,
  "next": "http://localhost:8000/api/v1/content/by_source/?source=weather&page=2",
  "previous": null,
  "results": [
    {
      "id": 10,
      "source": "weather",
      "source_display": "OpenWeather",
      "title": "Weather in London",
      "description": "Temperature: 15°C, Feels like: 13°C, Humidity: 72%, Pressure: 1013 hPa. Partly cloudy",
      "content_url": "",
      "image_url": "https://openweathermap.org/img/wn/02d@2x.png",
      "published_date": "2026-04-30T10:00:00Z",
      "fetched_at": "2026-04-30T10:00:00Z"
    }
  ]
}
```

## Error Responses

### 400 Bad Request

```json
{
  "error": "Invalid request parameters"
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse. Default limits:
- Anonymous users: 100 requests per hour
- Authenticated users: 1000 requests per hour

## Pagination

All list endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

## Filtering and Search

Content endpoints support:
- **Filtering**: Use query parameters to filter by specific fields
- **Search**: Use `search` parameter to search across title and description
- **Ordering**: Use `ordering` parameter with field name (prefix with `-` for descending)

## Caching

API responses are cached for 15 minutes to improve performance. Cache is automatically invalidated when new data is fetched.

## Interactive Documentation

Visit `/api/docs/` for interactive Swagger UI documentation where you can test all endpoints directly from your browser.
