from django.views import generic
from .models import Products


class ProductPage(generic.ListView):
    model = Products
    template_name = "product_page.html"
    context_object_name = 'products'
