from django.contrib import admin

# Register your models here.
from webtest.models import Event,Guest
class EventAdmin(admin.ModelAdmin):
    list_display=['id','name','status','address','start_time']

class GuestAdmin(admin.ModelAdmin):
    list_play=['realname','phone','email','sign','create_time']
    
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)
    
