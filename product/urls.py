from . import views
from django.urls import path

urlpatterns = [
     path('', views.ProductPage.as_view(), name='products'),
]
