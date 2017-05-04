import thread
from dateutil.parser import parse
import pytz
import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from inspect import currentframe

from django.db.models import Q

from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template import loader, Context
from django.utils.html import strip_tags
from reservation.settings import EMAIL_SEND_AS_USER
from django.core.mail import EmailMultiAlternatives


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reservation.settings import CLIENT_APP_CONFIG

from django.contrib.auth.models import User, Group
from resources.models import Blade, Chassis
from .models import Record
from base.models import Preference

from base.views import get_user


# Utility functions

def get_display_name(user):
    name = user.first_name + ' ' + user.last_name
    display_user_name = ''
    if name == ' ':
        display_user_name = user.username
    else:
        display_user_name = name
    return display_user_name


def get_user_visible_blades(user):
    blade_list = []
    for group in user.groups.all():
        blade_list.extend(Blade.objects.filter(group=group.id))
    return blade_list


# def send_notification_mail(user, current_record,prev_record):
def send_notification_mail(user, current_record):
    
    recepients = []
    prev_records = Record.objects.filter(
        blade=current_record.blade,
        end_time__lte=current_record.start_time).order_by('-start_time')
    print prev_records
    recepients.append(user)
    if len(prev_records) > 0:
        if current_record.user.id != prev_records[0].user.id:
            recepients.append(User.objects.get(id=prev_records[0].user.id))
    

    # Compose the email
    for recepient in recepients:
        # Create query
        query = Q()
        for group in recepient.groups.all():
            query |= Q(blade__group=group)

        # Get records sorted in decending order by id
        record_list = Record.objects.filter(query).order_by('-id')[:5]

        try:
            # if preference exists
            preference = Preference.objects.get(user=recepient.id)
            # temporary storing the currernt start time and end time ... so
            # that it will be not added multiple time for each user
            start_time = current_record.start_time
            end_time = current_record.end_time
            # update current_records
            if preference.timezone_positive:
                current_record.start_time = start_time + \
                    datetime.timedelta(hours=preference.timezone_hours, minutes=preference.timezone_minutes)
                current_record.end_time = end_time + \
                    datetime.timedelta(hours=preference.timezone_hours, minutes=preference.timezone_minutes)
            else:
                current_record.start_time = start_time - \
                    datetime.timedelta(hours=preference.timezone_hours, minutes=preference.timezone_minutes)
                current_record.end_time = end_time - \
                    datetime.timedelta(hours=preference.timezone_hours, minutes=preference.timezone_minutes)

            # update 5 records
            for record in record_list:
                if preference.timezone_positive:
                    record.start_time += datetime.timedelta(
                        hours=preference.timezone_hours, minutes=preference.timezone_minutes)
                    record.end_time += datetime.timedelta(
                        hours=preference.timezone_hours, minutes=preference.timezone_minutes)
                else:
                    record.start_time -= datetime.timedelta(
                        hours=preference.timezone_hours, minutes=preference.timezone_minutes)
                    record.end_time -= datetime.timedelta(
                        hours=preference.timezone_hours, minutes=preference.timezone_minutes)

        except:
            # no preference
            pass

        template = loader.get_template('send_mail.html')

        html_message = template.render({
            'user': user,
            'record_list': record_list,
            'current_record': current_record,
            'recepient': recepient,
            'AppConfig': CLIENT_APP_CONFIG,
        }
        )

        # added new thing ..!!
        if preference.dl_group != '':
            msg = EmailMultiAlternatives(
                'Reservation App Notification',
                'text_content',
                EMAIL_SEND_AS_USER,
                (preference.dl_group,
                 ))
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            break

        if preference.mail_status:
            msg = EmailMultiAlternatives(
                'Reservation App Notification',
                'text_content',
                EMAIL_SEND_AS_USER,
                (recepient.email,
                 ))
            msg.attach_alternative(html_message, "text/html")
            msg.send()

        # re-assigning the actual value of start_time and end_time
        current_record.start_time = start_time
        current_record.end_time = end_time


# Create your views here.
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def record_submit(request):
    # Get the user
    user = get_user(request.user.id)

    # Get blade
    blade = Blade.objects.get(pk=request.data['blade_id'])

    # Get start time
    start_time = parse_datetime(request.data['start_time'])
    start_time = start_time.replace(microsecond=0)
    # Get end time
    end_time = parse_datetime(request.data['end_time'])
    end_time = end_time.replace(microsecond=0)

    query = Q(blade=blade) & ((Q(start_time__gt=start_time) & Q(start_time__lt=end_time)) | (
        Q(end_time__lt=end_time) & Q(end_time__gt=start_time)) | (Q(start_time__lt=start_time) & Q(end_time__gt=end_time)))

    records = Record.objects.filter(query)

    if len(records) > 0:
        # not allowed to reserve
        return Response({
            'status': 'failed',
            'user': get_display_name(records[0].user),
            'chassis_name': records[0].blade.chassis.name,
            'chassis_hostname': records[0].blade.chassis.hostname,
            'blade_name': records[0].blade.name,
            'start_time': records[0].start_time,
            'end_time': records[0].end_time
        })

    if start_time >= end_time:
        return Response({
            'status': 'invalid_input',
            'user': get_display_name(user),
            'chassis_name': blade.chassis.name,
            'chassis_hostname': blade.chassis.hostname,
            'blade_name': blade.name,
            'start_time': start_time,
            'end_time': end_time
        })

    # prev_record = Record.objects.get(blade = blade)
    new_record = Record(
        user=user,
        blade=blade,
        start_time=start_time,
        end_time=end_time)
    new_record.save()

    try:
        thread.start_new_thread(send_notification_mail, (user, new_record))
    except:
        pass

    return Response({
        'status': 'success',
        'user': get_display_name(new_record.user),
        'chassis_name': new_record.blade.chassis.name,
        'chassis_hostname': new_record.blade.chassis.hostname,
        'blade_name': new_record.blade.name,
        'start_time': new_record.start_time,
        'end_time': new_record.end_time
    })


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def records_view_get(request):
    # import pdb 
    # pdb.set_trace()

    # Get the user
    user = get_user(request.user.id)

    # Create query
    query = Q()
    try:
        qstr = request.query_params.get('search_string')
    except:
        qstr = ''
    

    for group in user.groups.all():
        query |= Q(blade__group=group)
        print group,"here i printed the group"

    query &= Q(start_time__gte=timezone.now() - datetime.timedelta(days=30))
    if qstr is not None:
        query &= (
            Q(
                blade__chassis__name__contains=qstr) | Q(
                blade__chassis__hostname__contains=qstr) | Q(
                blade__name__contains=qstr) | Q(
                    user__first_name__icontains=qstr) | Q(
                        user__last_name__icontains=qstr) | Q(
                            start_time__contains=qstr) | Q(
                                end_time__contains=qstr))

    # Get records sorted in decending order by id
    records_list = Record.objects.filter(query).order_by('-id')
    for i in records_list:
        print i,"rpinted records belonging to you ..."
    paginator = Paginator(records_list, 5)

    page = 1
    try:
        page = request.query_params.get('page')
        records = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        records = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.num_pages
        records = paginator.page(page)

    result = {
        'page': page,
        'num_pages': paginator.num_pages,
        'total_records': len(records_list),
        'records_per_page': 5,
        'records': []
    }

    for record in records:
        result['records'].append({
            'chassis': record.blade.chassis.name,
            'hostname': record.blade.chassis.hostname,
            'blade': record.blade.name,
            'user': get_display_name(record.user),
            'userid': record.user.id,
            'start_time': record.start_time,
            'end_time': record.end_time,
            'record': record.id
        })

    return Response(result)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def list_view_get(request):
    result_dict = {}
    utc = timezone.now()

    # Get the user
    user = get_user(request.user.id)
    blade_list = get_user_visible_blades(user)

    for blade in blade_list:
        result_dict[blade] = {
            'chassis': blade.chassis.name,
            'chassis_id': blade.chassis.id,
            'hostname': blade.chassis.hostname,
            'chassis_comment': blade.chassis.comment,
            'blade': blade.name,
            'blade_id': blade.id,
            'user': '',
            'date': '',
            'start_time': '',
            'end_time': '',
            'record': -1,
            'status': 'free',
            'comment': blade.comment
        }

        records_reserved = Record.objects.filter(
            blade=blade, end_time__gt=utc).order_by('-id')

        # Blade is currently reserved
        for record in records_reserved.filter(start_time__lte=utc):
            result_dict[blade] = {
                'chassis': blade.chassis.name,
                'chassis_id': blade.chassis.id,
                'hostname': blade.chassis.hostname,
                'chassis_comment': blade.chassis.comment,
                'blade': blade.name,
                'blade_id': blade.id,
                'user': get_display_name(record.user),
                'start_time': record.start_time,
                'end_time': record.end_time,
                'record': record.id,
                'status': 'reserved',
                'comment': blade.comment,
            }

        # Blade is reserved for future
        record = records_reserved.filter(
            start_time__gt=utc).order_by('start_time')
        if(len(record) != 0 and result_dict[blade]['status'] == "free"):
            result_dict[blade] = {
                'chassis': blade.chassis.name,
                'chassis_id': blade.chassis.id,
                'hostname': blade.chassis.hostname,
                'chassis_comment': blade.chassis.comment,
                'blade': blade.name,
                'blade_id': blade.id,
                'user': get_display_name(record[0].user),
                'start_time': record[0].start_time,
                'end_time': record[0].end_time,
                'record': record[0].id,
                'status': 'reserved_for_future',
                'comment': blade.comment,
            }

    result = [result_dict[x] for x in result_dict]
    return Response(result)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def calendar_view(request):

    blade_id = request.GET.get('blade_id')

    # current date time from client with time 00:00
    start_date_time = request.GET.get('date')
    start_date_time = datetime.datetime.strptime(
        start_date_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    start_date_time = start_date_time.replace(tzinfo=pytz.UTC)
    end_date_time = start_date_time + datetime.timedelta(hours=23, minutes=59)
    end_date_time = end_date_time.replace(tzinfo=pytz.UTC)

    result = []

    query = Q(
        blade_id=blade_id) & Q(
        start_time__gte=start_date_time) & Q(
            end_time__lte=end_date_time)
    records = Record.objects.filter(query)
    # records = Record.objects.filter()

    k = 0
    for i in records:
        result.insert(k, {
            'name': i.blade.name,
            'start_time': i.start_time,
            'end_time': i.end_time,
            'case': 1,
            'user_name': i.user.username,
        })
        k += 1

    # when st_datet=_time is less than current time but end_date_time is less
    # than
    query = Q(
        blade_id=blade_id) & Q(
        start_time__lte=start_date_time) & Q(
            end_time__gte=start_date_time) & Q(
                end_time__lte=end_date_time)
    records = Record.objects.filter(query)
    for i in records:
        result.insert(k, {
            'name': i.blade.name,
            'start_time': i.start_time,
            'end_time': i.end_time,
            'case': 2,
            'user_name': i.user.username,
        })
        k += 1

    # when st_date_time is in between start time and end time but end_time is
    # greater than today end time
    query = Q(
        blade_id=blade_id) & Q(
        start_time__lte=end_date_time) & Q(
            end_time__gte=end_date_time) & Q(
                start_time__gte=start_date_time)
    records = Record.objects.filter(query)
    for i in records:
        result.insert(k, {
            'name': i.blade.name,
            'start_time': i.start_time,
            'end_time': i.end_time,
            'case': 3,
            'user_name': i.user.username,
        })
        k += 1

    # when st_date_time is less than start_time and end_date_time is gt than
    # end_time
    query = Q(
        blade_id=blade_id) & Q(
        start_time__lte=start_date_time) & Q(
            end_time__gte=end_date_time)
    records = Record.objects.filter(query)
    for i in records:
        result.insert(k, {
            'name': i.blade.name,
            'start_time': i.start_time,
            'end_time': i.end_time,
            'case': 4,
            'user_name': i.user.username,
        })
        k += 1

    return Response(result)
