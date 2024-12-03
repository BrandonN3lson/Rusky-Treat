from .views import product_detail
from django.urls import path
from .views import ProductPage, DeleteProduct, add_product

urlpatterns = [
     path('add-product/', add_product, name='add_product'),
     path('', ProductPage.as_view(), name='products'),
     path('delete-product/<int:product_id>/', DeleteProduct.as_view(),
          name='delete_product'),
     path('products/<slug:category_slug>/', ProductPage.as_view(),
          name='product_category'
          ),
     path('<slug:slug>/', product_detail, name='product_detail'),
]
