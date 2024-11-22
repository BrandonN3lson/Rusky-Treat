from .views import OrderPage
from django.urls import path
from .views import AddToCart, RemoveFromCart

urlpatterns = [
     path("", OrderPage.as_view(), name="orders"),
     path('add-to-cart/<int:product_id>/', AddToCart.as_view(),
          name='add_to_cart'),
     path('remove-from-cart/<int:product_id>/', RemoveFromCart.as_view(),
          name="remove_from_cart")
]
