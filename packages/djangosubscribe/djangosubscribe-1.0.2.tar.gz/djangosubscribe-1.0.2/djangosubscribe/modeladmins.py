from django.contrib.admin import ModelAdmin
from djangosubscribe.models import SubscriberModel


class SubscriberModelAdmin(ModelAdmin):
    list_display = ['email', 'pk', 'username']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['username', 'first_name', 'last_name']