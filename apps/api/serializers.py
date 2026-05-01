from rest_framework import serializers
from apps.integrations.models import AggregatedContent


class AggregatedContentSerializer(serializers.ModelSerializer):
    source_display = serializers.CharField(source='get_source_display', read_only=True)

    class Meta:
        model = AggregatedContent
        fields = (
            'id',
            'source',
            'source_display',
            'title',
            'description',
            'content_url',
            'image_url',
            'published_date',
            'fetched_at',
        )
        read_only_fields = ('id', 'fetched_at')


class AggregatedContentDetailSerializer(serializers.ModelSerializer):
    source_display = serializers.CharField(source='get_source_display', read_only=True)

    class Meta:
        model = AggregatedContent
        fields = '__all__'
        read_only_fields = ('id', 'fetched_at')
