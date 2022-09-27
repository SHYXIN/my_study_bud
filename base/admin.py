from django.contrib import admin

# Register your models here.
from .models import Room,Topic,Message, User

class UserAdmin(admin.ModelAdmin):
    exclude = ['password']
    

admin.site.register(User, UserAdmin)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)