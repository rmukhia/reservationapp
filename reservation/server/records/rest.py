from rest_framework import serializers, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from django.contrib.auth.models import User, Group

from base.rest import SearchViewSet

from resources.models import Blade
from .models import Record

'''
Record rest_framework
'''
class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Record
        fields = ('url', 'id', 'start_time', 'end_time', 'blade', 'user')


class RecordViewSet(viewsets.ModelViewSet, SearchViewSet):
    queryset = Record.objects.all()
    model = Record
    serializer_class = RecordSerializer

