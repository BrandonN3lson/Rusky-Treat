from django.urls import path
from .views import IndexPage, DeleteCategory, add_category

urlpatterns = [
     path('', IndexPage.as_view(), name='index'),
     path('add_category/', add_category, name="add_category"),
     path('delete-category/<str:category_title>/', DeleteCategory.as_view(),
          name='delete_category'),
]
