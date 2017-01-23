from django_filters.rest_framework import FilterSet, DateFilter, DateRangeFilter

from core.models import Measurement


__all__ = ('MeasurementDateFilter',)


class MeasurementDateFilter(FilterSet):
    # start_date = DateFilter(name='date',lookup_type=('gt'),)
    # end_date = DateFilter(name='date',lookup_type=('lt'))
    date_range = DateRangeFilter(name='created')

    class Meta:
        model = Measurement
        fields = ('created',)
