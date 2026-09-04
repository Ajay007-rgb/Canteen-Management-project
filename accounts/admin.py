from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_admin', 'created_at')
    list_filter = ('is_admin',)
    search_fields = ('user__username', 'user__email', 'phone_number')
