from django.contrib import admin

# Register your models here.
from accounts.models import User, Profile, PasswordReset

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(PasswordReset)