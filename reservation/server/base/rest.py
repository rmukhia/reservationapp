from rest_framework import serializers, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.core.exceptions import MultipleObjectsReturned
from .models import Preference
from django.contrib.auth.models import User, Group

'''
Custom search url
'''
class SearchViewSet(object):
    @list_route(methods=['get'])
    def search(self, request):
        # Get params 
        params = request.query_params.dict()
       
        # Remove the format params
        if 'format' in params.keys():
            del params['format']
        # many = False;
        try:
            obj = [self.model.objects.get(**params),]
        except MultipleObjectsReturned:
            obj = self.model.objects.filter(**params)
            # many = True;
        except:
            return Response({'url' :  'failed'})
        serializer = self.get_serializer(obj, many = True)
        return Response(serializer.data)

'''
User rest_framework
'''
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email', 'groups', 'is_staff')


class UserViewSet(viewsets.ReadOnlyModelViewSet, SearchViewSet):
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer

'''
Group rest_framework
'''

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'id', 'name')


class GroupViewSet(viewsets.ReadOnlyModelViewSet, SearchViewSet):
    queryset = Group.objects.all()
    model = Group
    serializer_class = GroupSerializer

'''
Prefrence rest_framework
'''

class PreferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Preference
        fields = ('url', 'id', 'user','timezone_positive', 'timezone_hours' , 'timezone_minutes','image','mail_status','dl_group')


class PreferenceViewSet(viewsets.ModelViewSet, SearchViewSet):
    queryset = Preference.objects.all()
    model = Preference
    serializer_class = PreferenceSerializer

'''
Prefrence rest_framework
'''

