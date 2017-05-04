"""reservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
1. Add an import:  from my_app import views
2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
1. Add an import:  from other_app.views import Home
2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
1. Import the include() function: from django.conf.urls import url, include
2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from reservation.settings import REST_API_URL_BASE
from django.conf import settings
from django.conf.urls.static import static

# Import Base; contains User and Group
import base.views
import base.rest

# Import Resources; contain Chassis and Blade
import resources.rest

# Import Records; contain Record
import records.rest


router = routers.DefaultRouter()

router.register(r'records', records.rest.RecordViewSet)
router.register(r'chassis', resources.rest.ChassisViewSet)
router.register(r'blades', resources.rest.BladeViewSet)
router.register(r'users', base.rest.UserViewSet)
router.register(r'groups', base.rest.GroupViewSet)
router.register(r'preferences', base.rest.PreferenceViewSet)
# should needed in rest-api to display
# router.register(r'preferences', base.rest.PreferenceViewSet)
# router.register(r'preferences', base.rest.PreferenceViewSet)

'''
Routing
'''

urlpatterns = [
    url(r'^' + REST_API_URL_BASE + r'/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('base.urls', namespace='base')),
    url(r'^', include('records.urls', namespace='rcords')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

