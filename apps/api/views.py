from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from apps.integrations.models import AggregatedContent
from .serializers import AggregatedContentSerializer, AggregatedContentDetailSerializer
from .filters import AggregatedContentFilter


class AggregatedContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AggregatedContent.objects.select_related().all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AggregatedContentFilter
    search_fields = ['title', 'description']
    ordering_fields = ['published_date', 'fetched_at']
    ordering = ['-published_date']  # newest first

    def get_serializer_class(self):
        # use detailed serializer for single item view
        if self.action == 'retrieve':
            return AggregatedContentDetailSerializer
        return AggregatedContentSerializer

    @method_decorator(cache_page(60 * 15))  # cache for 15 min
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def by_source(self, request):
        source = request.query_params.get('source')
        if not source:
            return Response({'error': 'Source parameter is required'}, status=400)

        cache_key = f'content_by_source_{source}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset().filter(source=source))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            cache.set(cache_key, response.data, 60 * 15)
            return response

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, 60 * 15)
        return Response(serializer.data)

