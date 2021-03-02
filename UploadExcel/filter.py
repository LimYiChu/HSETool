import django_filters

from .models import *

class ActionItemsFilter(django_filters.FilterSet):
    class Meta:
        model= ActionItems
        fields= '__all__'
