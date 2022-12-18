import django_filters
from django_filters import FilterSet

from images.models import Images


class ImagesFilter(FilterSet):
    name = django_filters.CharFilter(
        field_name='people__name', lookup_expr='istartswith')

    class Meta:
        model = Images
        fields = ('location', 'date', 'name')
