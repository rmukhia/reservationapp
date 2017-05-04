from django.contrib import admin
from .models import Record


class Record_view(admin.ModelAdmin):
	list_display = ['user','blade','start_time','end_time']
	class Meta:
		model = Record
admin.site.register(Record,Record_view)

# Register your models here.
