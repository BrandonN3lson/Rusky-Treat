from django.contrib import admin
from .models import Product
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    list_display = ('name', 'slug', 'category', 'created_on')
    search_fields = ['name', 'category__name']
    list_filter = ('category', 'created_on')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('description',)
