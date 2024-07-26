from django.contrib import admin
from .models import Profile



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'age', 'is_sub', 'uuid']
    list_filter = ["is_sub"]
    autocomplete_fields = ["user"]
