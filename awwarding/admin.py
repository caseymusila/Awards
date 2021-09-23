from cloudinary import import_django_settings
from django.contrib import admin
from .models import Profile, Project

# Register your models here.
admin.site.register(Profile)
admin.site.register(Project)

