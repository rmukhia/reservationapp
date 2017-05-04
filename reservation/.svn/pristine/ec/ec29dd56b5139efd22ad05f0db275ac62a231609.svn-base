import fnmatch
import time
import os
from reservation.settings import ANGULARJS_DIR, CLIENT_APP_CONFIG
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .models import Preference

# Utility functions


def get_user(user_id):
    user = User.objects.get(pk=user_id)
    return user


def get_files(path, extenstion):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.' + extenstion):
            matches.append(os.path.relpath(os.path.join(root, filename), path))
    return matches

# Create your views here.


def index(request):
    CLIENT_APP_CONFIG['angular_files'] = get_files(ANGULARJS_DIR, 'js')
    CLIENT_APP_CONFIG['css_files'] = get_files(ANGULARJS_DIR, 'css')
    return render(request, 'index.htm', {'AppConfig': CLIENT_APP_CONFIG})


def client_appconfig(request):
    return render(request, 'app-config.js', {'AppConfig': CLIENT_APP_CONFIG})


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def logged_in(request):
    # time.sleep(5)
    content = {
        'id': unicode(request.user.id),
        'username': unicode(request.user.username),
        'first_name': unicode(request.user.first_name),
        'last_name': unicode(request.user.last_name),
        'email': unicode(request.user.email),
        'groups': [{'id': unicode(g.id), 'name': unicode(g)} for g in request.user.groups.all()]
    }
    return Response(content)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def preference_submit(request):
    # Get the user
    # user = get_user(request.user.id)
    preference = None
    if request.data['timezone_positive'] == "true":
        timezone_positive = True
    else:
        timezone_positive = False
    timezone_hours = request.data['timezone_hours']
    timezone_minutes = request.data['timezone_minutes']
    if request.data['notification_status'] == "true":
        mail_status = True
    else:
        mail_status = False
    print request.data,"printed the dl_group here ..."
    dl_group = request.data['dl_group']

    try:
        preference = Preference.objects.get(user=request.user.id)
        preference.timezone_positive = timezone_positive
        preference.timezone_hours = timezone_hours
        preference.timezone_minutes = timezone_minutes
        preference.mail_status = mail_status
        preference.dl_group = dl_group
    except:
        preference = Preference(user=User.objects.get(pk=request.user.id),
                                timezone_positive=timezone_positive,
                                timezone_hours=timezone_hours,
                                timezone_minutes=timezone_minutes,
                                mail_status=mail_status,
                                dl_group=dl_group)

    preference.save()

    return Response({"status": "success"})


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def basic_info_submit(request):
     # Get the user

    user = User.objects.get(pk=request.user.id)
    user.first_name = request.data['first_name']
    user.last_name = request.data['last_name']
    user.email = request.data['email']

    user.save()

    return Response({"status": "success"})


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def password_submit(request):
     # Get the user
    user = User.objects.get(pk=request.user.id)
    user.set_password(request.data['password'])
    user.save()
    return Response({"status": "success"})


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def image_submit(request):
    preference = Preference.objects.get(user=request.user.id)
    preference.image = request.FILES['file']
    preference.save()
    return Response({'data': 'a'})
