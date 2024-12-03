# views.py
from django.views import generic, View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category
from .forms import AddProductForm
from category.forms import AddCategoryForm


class ProductPage(generic.ListView):
    model = Product
    template_name = "product_page.html"
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_product_form = AddProductForm()

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
        context['add_product_form'] = add_product_form
        return context


class DeleteProduct(View):
    def get(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            category_slug = product.category.slug
        except Product.DoesNotExist:
            messages.error(request, 'Category doesnt exist')
            return redirect('index')
        product.delete()
        messages.success(request,
                         f'Product {product.name} has been deleted')
        return redirect('product_category', category_slug=category_slug)


def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


def add_product(request):
    add_category_form = AddCategoryForm()
    add_product_form = AddProductForm(request.POST, request.FILES)

    if request.method == 'POST':
        if add_product_form.is_valid():
            add_product_form.save()
            return redirect('index')
        else:
            messages.error(request, 'form is invalid')
    return render(request,
                  'index.html',
                  {
                    'add_category_form': add_category_form,
                    'add_product_form': add_product_form,
                    })
