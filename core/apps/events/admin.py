from django.contrib import admin

from core.apps.events.models import Condition, Event

# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'address', 'picture', 'created_at',
                    'updated_at', 'is_visible')
    filter_horizontal = ('participants', 'conditions')


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'is_visible', 'created_at', 'updated_at')
