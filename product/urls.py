from . import views
from django.urls import path
from .views import ProductPage

urlpatterns = [
     path('', views.ProductPage.as_view(), name='products'),
     path('products/<slug:category_slug>/', ProductPage.as_view(),
          name='product_category'
          ),
     path('<slug:slug>/', views.product_detail, name='product_detail'),
]
