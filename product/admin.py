from django.contrib import admin
from .models import Product
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    """
    Class: ProductAdmin
    - Customizes the Django admin interface for managing `Product` objects.

    Attributes:
    - list_display: Specifies the fields to display in the list view of the
                    admin panel.
    - search_fields: Defines the fields that can be searched in the admin
                     search bar.
    - list_filter: Enables filtering of products by category and created date
                   in the admin panel.
    - prepopulated_fields: Pre-populates the `slug` field based on the `name`
                           field for each product.
    - summernote_fields: Enables the Summernote rich-text editor for the
                         `description` field.
    """

    list_display = ('name', 'slug', 'category', 'created_on')
    search_fields = ['name', 'category__name']
    list_filter = ('category', 'created_on')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('description',)
