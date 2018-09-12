from django.contrib import admin
from .models import MyUser, FestaData, PiazzaData

# Register your models here.
admin.site.register(MyUser)
admin.site.register(FestaData)
admin.site.register(PiazzaData)