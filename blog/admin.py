from django.contrib import admin
from .models import blogsite_post

from accounts.models import userProfile



# Register your models here.
admin.site.register(blogsite_post)  # Register your models here, e.g., admin.site.register(YourModel)
admin.site.register(userProfile)  # Register the user_profile model