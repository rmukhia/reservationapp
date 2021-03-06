from rest_framework import serializers, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from django.contrib.auth.models import User, Group


'''
User REST rest_framework
'''
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Returns specific instances of users
    @list_route(methods=['get'])
    def search(self, request):
        # Get params 
        params = request.query_params.dict()
       
        # Remove the format params
        if 'format' in params.keys():
            del params['format']

        try:
            user = User.objects.get(**params)
        except:
            return Response(['Failed'])
        serializer = self.get_serializer(user)
        return Response(serializer.data)



'''
Group rest_framework
'''

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'id', 'name')


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # Returns specific instances of users
    @list_route(methods=['get'])
    def search(self, request):
        # Get params 
        params = request.query_params.dict()
        
        # Remove the format params
        if 'format' in params.keys():
            del params['format']

        try:
            group = Group.objects.get(**params)
        except:
            return Response(['Failed'])
        serializer = self.get_serializer(group)
        return Response(serializer.data)