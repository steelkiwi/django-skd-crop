from django.contrib import admin

from .models import UserProfile, ChildProfile, Profile

admin.site.register(UserProfile)
admin.site.register(ChildProfile)
admin.site.register(Profile)
