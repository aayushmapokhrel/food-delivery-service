from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import path
from django.shortcuts import render
from restaurants.models import Restaurant
from orders.models import Order

User = get_user_model()

class CustomAdminSite(AdminSite):
    site_header = "Food Delivery Dashboard"
    site_title = "Admin Dashboard"
    index_title = "Welcome to the Food Delivery Admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.admin_dashboard), name="admin-dashboard"),
        ]
        return custom_urls + urls

    def admin_dashboard(self, request):
        total_users = User.objects.count()
        total_restaurants = Restaurant.objects.count()
        total_orders = Order.objects.count()
        order_statuses = Order.objects.values('status').annotate(count=Count('status'))

        context = {
            "total_users": total_users,
            "total_restaurants": total_restaurants,
            "total_orders": total_orders,
            "order_statuses": order_statuses,
        }
        return render(request, "admin/dashboard.html", context)

custom_admin_site = CustomAdminSite(name="custom_admin")
