from django.contrib import admin

from .models import Profile

admin.site.site_header = 'Taipei Language Institute'

admin.site.register(Profile)