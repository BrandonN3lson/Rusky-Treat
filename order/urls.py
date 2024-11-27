from .views import OrderPage
from django.urls import path
from .views import AddToCart, RemoveFromCart, UpdateProductQuantity
from .views import SubmitOrder, EditOrder

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
     path('<int:order_id>/edit/',
          EditOrder.as_view(), name='edit_order')
]
