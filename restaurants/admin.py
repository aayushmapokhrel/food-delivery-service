from django.contrib import admin
from restaurants.models import Restaurant, Category, MenuItem


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "name", "address", "phone")
    search_fields = ("name", "owner__email")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "name")


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "name", "price", "available")
    list_filter = ("available",)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
