# views.py
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


class ProductPage(generic.ListView):
    model = Product
    template_name = "product_page.html"
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if category_slug is passed in URL
        category_slug = self.kwargs.get('category_slug')

        # Fetch categories
        categories = Category.objects.all()
        products_by_category = {}

        if category_slug:
            # Filter products by the specific category
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
            products_by_category[category.title] = products
        else:
            # Group all products by category if no category slug is specified
            for category in categories:
                products = Product.objects.filter(category=category)
                products_by_category[category.title] = products

        context['products_by_category'] = products_by_category
        context['categories'] = categories
        return context


def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})
