from __future__ import unicode_literals

from django.db import models
import django.contrib.auth.models as auth_models

# Create your models here.

Blank = " "
class Chassis(models.Model):
	name = models.CharField(max_length=255)
	hostname = models.CharField(max_length=50)
	comment = models.CharField(max_length = 80,default = None,blank = True)

	def __str__(self):
		return self.name + ':' + self.hostname

	class Meta:
		app_label = 'resources'
	

class Blade(models.Model):
	name = models.CharField(max_length=255)
	chassis = models.ForeignKey(Chassis)
	group = models.ForeignKey(auth_models.Group)
	comment = models.TextField(default=None,blank=True)

	def __str__(self):
		return self.chassis.name + ':' + self.name

	class Meta:
		app_label = 'resources'
	
