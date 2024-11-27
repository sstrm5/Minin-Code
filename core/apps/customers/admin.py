from django.contrib import admin

from core.apps.customers.models import Customer

# Register your models here.
@admin.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')