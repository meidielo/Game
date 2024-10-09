from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "password", "confirm_password"]
    search_fields = ["username"]
# admin.site.register(Profile,ProfileAdmin)