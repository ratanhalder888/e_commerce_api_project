from django.contrib import admin
from . models import Order, OrderItem

# Register your models here.

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user_username', 'user_email']
    inlines = [OrderItemInLine]
    readonly_fields = ['total_amount']