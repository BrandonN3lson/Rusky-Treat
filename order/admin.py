from django.contrib import admin
from .models import Order, OrderItem
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Order)
class OrderAdmin(SummernoteModelAdmin):
    list_display = ('id', 'user', 'order_date', 'status')
    search_fields = ['user', 'status']
    list_filter = ('status',)


@admin.register(OrderItem)
class OrderItemAdmin(SummernoteModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total_price')

    def save_model(self, request, obj, form, change):
        # Automatically calculate total_price based on
        #  product price and quantity
        obj.total_price = obj.product.price * obj.quantity
        super().save_model(request, obj, form, change)
