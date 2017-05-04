from django.contrib import admin
from .models import Preference


class Preference_view(admin.ModelAdmin):
	list_display = ['user','timezone_positive' , 'timezone_hours', 'timezone_minutes','dl_group']
	class Meta:
		model = Preference

admin.site.register(Preference, Preference_view)