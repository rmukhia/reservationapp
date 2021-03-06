from __future__ import unicode_literals
#import datetime
from django.db import models
import django.contrib.auth.models as auth_models
import resources.models as resource_models

class Record(models.Model):
	user = models.ForeignKey(auth_models.User)
	blade = models.ForeignKey(resource_models.Blade)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	def __str__(self):
		return str(self.user) +'|' + str(self.blade)

	class Meta:
		app_label = 'records'
	
# Create your models here.

