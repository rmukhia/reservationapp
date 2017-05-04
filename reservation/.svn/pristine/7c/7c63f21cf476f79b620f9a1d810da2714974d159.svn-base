from django.conf.urls import url
from reservation.settings import REST_API_URL_BASE
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^appconfig.js$', views.client_appconfig, name='client_appconfig'),
  url(r'^api-auth/logged_in$', views.logged_in, name = 'logged_in'),
  url(r'^%s/custom/preference_submit$' % REST_API_URL_BASE, views.preference_submit, name = 'preference_submit'),
  url(r'^%s/custom/basic_info_submit$' % REST_API_URL_BASE, views.basic_info_submit, name = 'basic_info_submit'),
  url(r'^%s/custom/password_submit$' % REST_API_URL_BASE, views.password_submit, name = 'password_submit'),
  url(r'^%s/custom/image_submit$' % REST_API_URL_BASE, views.image_submit, name = 'password_submit'),
  ]