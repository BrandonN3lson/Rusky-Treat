from . import views
from django.urls import path

urlpatterns = [
     path('', views.AboutPage.as_view(), name='about'),
]
