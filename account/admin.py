from django.contrib import admin
from models import UserProfile
from django.contrib.auth.models import User

#class UserProfileInline(admin.StackedInline):
#    model = UserProfile
#    extra = 1
#
#class UserAdmin(admin.ModelAdmin):
#    inlines = [UserProfileInline, ]

admin.site.register(UserProfile)
