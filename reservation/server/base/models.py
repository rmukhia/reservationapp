from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from reservation.settings import MEDIAFILES_DIRS
# Create your models here.

def content_file_name(instance, filename):
	fname = filename.split('.')
	fname[0] = instance.user.username + '.' + fname[1]
	return '/'.join(['image',fname[0]])

class Preference(models.Model):
	user = models.ForeignKey(User)

	timezone_positive = models.BooleanField()
	timezone_hours = models.SmallIntegerField()
	timezone_minutes = models.SmallIntegerField()
	mail_status = models.BooleanField(default = True)
	dl_group = models.CharField(max_length = 70,blank = True)
	image = models.ImageField(upload_to=content_file_name)

	def __str__(self):
		return self.user.username

	class Meta:
		app_label = 'base'
