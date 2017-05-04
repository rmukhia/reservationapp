from django.contrib import admin
from .models import Chassis, Blade

admin.site.register(Chassis)
# admin.site.register(Blade)


# Register your models here.
class Blade_View(admin.ModelAdmin):
	list_display = ['chassis','name']
	class Meta:
		model = Blade
admin.site.register(Blade,Blade_View)
