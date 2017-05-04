from rest_framework import serializers, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from django.contrib.auth.models import Group

from base.rest import SearchViewSet

from .models import Chassis, Blade


'''
Chassis rest_framework
'''
# Serializers define the API representation.
class ChassisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chassis
        fields = ('url', 'id', 'name', 'hostname')

# ViewSets define the view behavior.
class ChassisViewSet(viewsets.ReadOnlyModelViewSet, SearchViewSet):
    queryset = Chassis.objects.all()
    model = Chassis
    serializer_class = ChassisSerializer


'''
Blade rest_framework
'''
# Serializers define the API representation.
class BladeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blade
        fields = ('url', 'id', 'name', 'chassis', 'group', 'comment')

# ViewSets define the view behavior.
class BladeViewSet(viewsets.ReadOnlyModelViewSet, SearchViewSet):
    queryset = Blade.objects.all()
    model = Blade
    serializer_class = BladeSerializer

