from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AggregatedContentViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'content', AggregatedContentViewSet, basename='content')

urlpatterns = [
    path('', include(router.urls)),
]
