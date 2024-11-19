from . import views
from django.urls import path

urlpatterns = [
     path("", views.OrderPage.as_view(), name="orders"),
]
