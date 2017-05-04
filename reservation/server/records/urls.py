from django.conf.urls import url
from reservation.settings import REST_API_URL_BASE
from . import views

urlpatterns = [
  url(r'^%s/custom/list_view$' % REST_API_URL_BASE, views.list_view_get, name = 'list_view_get'),
  url(r'^%s/custom/records_view$' % REST_API_URL_BASE, views.records_view_get, name = 'records_view_get'),
  url(r'^%s/custom/record_submit$' % REST_API_URL_BASE, views.record_submit, name = 'record_submit'),
  url(r'^%s/custom/calendar_view$' % REST_API_URL_BASE, views.calendar_view, name = 'calendar_view'),
 
  ]