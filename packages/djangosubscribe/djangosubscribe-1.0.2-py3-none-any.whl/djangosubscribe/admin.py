from django.contrib import admin
from djangosubscribe.models import SubscriberModel
from djangosubscribe.modeladmins import SubscriberModelAdmin


# Register your models here.
admin.site.register(SubscriberModel, SubscriberModelAdmin)
