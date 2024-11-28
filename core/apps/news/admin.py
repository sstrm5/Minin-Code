from django.contrib import admin

from core.apps.news.models import News

# Register your models here.


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'created_at',
                    'updated_at', 'is_published')
