from django.contrib import admin

from .models import User, FriendshipRequest, CustomUserManager

admin.site.register(User)
# admin.site.register(CustomUserManager)
admin.site.register(FriendshipRequest)
