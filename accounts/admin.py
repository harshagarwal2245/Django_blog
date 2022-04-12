from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo', 'experience')
    list_filter = ('date_of_birth',)
    search_fields = ('user',)

admin.site.register(Profile, ProfileAdmin)
# Register your models here.
