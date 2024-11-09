from django.shortcuts import render
from django.http import HttpResponse


def product_view(request):
    return HttpResponse("hello from products")
