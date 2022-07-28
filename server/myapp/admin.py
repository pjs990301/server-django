from django.contrib import admin

# Register your models here.
from .models import Users, Activity

admin.site.register(Users)
admin.site.register(Activity)
