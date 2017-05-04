import sqlite3
import  django.contrib.auth.models  as auth_models
from resources.models import *
from base.models import *

conn = sqlite3.connect("sqlite3.db")

for row in c.execute("SELECT *  FROM auth_group"):
	group = auth_models.Group(id=row[0], name=row[1])
	group.save()

for row in c.execute("SELECT *  FROM auth_user"):
	user = auth_models.User(password=row[1], is_superuser=row[3] , username= row[10], first_name = row[4], last_name= row[5], email = row[6], is_staff = row[7], is_active = row[8]) 
	user.save()

for row in c.execute("SELECT *  FROM resources_chassis")
	chassis = Chassis(name = row[1], hostname = row[2], comment = row[3])
	chassis.save()

for row in c.execute("SELECT *  FROM resources_blade")
	blade = Blade(name=row[1], chassis_id = 1, group_id = 1, comment =row[4])
	blade.save()

for user in auth_models.User.objects.all():
	pref = Preference(timezone_positive = True, timezone_hours = 5 ,timezone_minutes = 30, mail_status = True, user_id = user.id)
	pref.save()



