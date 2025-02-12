from django.contrib import admin
from orders.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'restaurant', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__email', 'restaurant__name')

admin.site.register(Order, OrderAdmin)
