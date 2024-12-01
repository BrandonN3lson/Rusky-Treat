from .views import OrderPage
from django.urls import path
from .views import AddToCart, RemoveFromCart, UpdateProductQuantity
from .views import SubmitOrder, EditOrder, ResubmitOrder
from .views import RemoveFromOrder, UpdateOrderQuantity, CancelEdit
from .views import CancelOrder, AdminOrderPage, ChangeOrderStatus

urlpatterns = [
     path("", OrderPage.as_view(), name="orders"),
     path('add-to-cart/<int:product_id>/', AddToCart.as_view(),
          name='add_to_cart'),
     path('remove-from-cart/<int:product_id>/', RemoveFromCart.as_view(),
          name="remove_from_cart"),
     path('update-product-quantity/<int:product_id>/',
          UpdateProductQuantity.as_view(), name='update_product_quantity'),
     path('submit-order/',
          SubmitOrder.as_view(), name='submit_order'),

     path("admin-orders/", AdminOrderPage.as_view(), name="admin_orders"),
     path("change-order-status/<int:order_id>", ChangeOrderStatus.as_view(),
          name="change_status"),

     path('<int:order_id>/edit/',
          EditOrder.as_view(), name='edit_order'),
     path('update-order-quantity/<int:order_id>/<int:product_id>/',
          UpdateOrderQuantity.as_view(), name='update_order_quantity'),
     path('remove-from-order/<int:order_id>/<int:product_id>/',
          RemoveFromOrder.as_view(), name='remove_from_order'),
     path('resubmit-order/<int:order_id>', ResubmitOrder.as_view(),
          name='resubmit_order'),
     path('cancel-edit/<int:order_id>', CancelEdit.as_view(),
          name='cancel_edit'),
     path('cancel-order/<int:order_id>', CancelOrder.as_view(),
          name='cancel_order'),

]
