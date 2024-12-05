from django.contrib import admin
from .models import Order, OrderItem
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Order)
class OrderAdmin(SummernoteModelAdmin):
    """
    OrderAdmin.

    Admin configuration for managing `Order` objects in the Django
    admin interface.

    Attributes:
        1. list_display: Specifies the fields to display in the admin
                              list view.
        2. search_fields: Allows searching by user and status fields
                                 in the admin.
        list_filter: Enables filtering the orders by their status
                             in the admin.
    """

    list_display = ('id', 'user', 'order_date', 'status')
    search_fields = ['user', 'status']
    list_filter = ('status',)


@admin.register(OrderItem)
class OrderItemAdmin(SummernoteModelAdmin):
    """
    OrderItemAdmin.

    Admin configuration for managing `OrderItem` objects in the Django
    admin interface.

    Attributes:
        list_display: Specifies the fields to display in the admin
                      list view (e.g., order, product, quantity,
                      and total price).

    Methods:
        save_model(request, obj, form, change):
            Automatically calculate total_price based on
            product price and quantity
"""

    list_display = ('order', 'product', 'quantity', 'total_price')

    def save_model(self, request, obj, form, change):

        obj.total_price = obj.product.price * obj.quantity
        super().save_model(request, obj, form, change)
