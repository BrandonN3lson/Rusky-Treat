# from django.shortcuts import render
from django.views import generic
from .models import Category


class IndexPage(generic.ListView):
    model = Category
    template_name = "index.html"
    context_object_name = 'categories'
