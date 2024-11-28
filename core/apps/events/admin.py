from django.contrib import admin

from core.apps.events.models import Event

# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'address', 'picture', 'created_at',
                    'updated_at', 'is_visible')
