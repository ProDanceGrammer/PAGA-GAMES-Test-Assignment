from django_filters import rest_framework as filters
from apps.integrations.models import AggregatedContent


class AggregatedContentFilter(filters.FilterSet):
    source = filters.ChoiceFilter(choices=AggregatedContent.SOURCE_CHOICES)
    published_after = filters.DateTimeFilter(field_name='published_date', lookup_expr='gte')
    published_before = filters.DateTimeFilter(field_name='published_date', lookup_expr='lte')
    fetched_after = filters.DateTimeFilter(field_name='fetched_at', lookup_expr='gte')
    fetched_before = filters.DateTimeFilter(field_name='fetched_at', lookup_expr='lte')

    class Meta:
        model = AggregatedContent
        fields = ['source']
