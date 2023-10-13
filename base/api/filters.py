from django_filters.rest_framework import FilterSet, RangeFilter

from .. import models

class ItemFilterSet(FilterSet):
    harga = RangeFilter()
    class Meta:
        model = models.Item
        fields = '__all__'
        exclude = ['gambar']