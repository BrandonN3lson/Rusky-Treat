# views.py
from django.views import generic, View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category
from .forms import AddProductForm
from category.forms import AddCategoryForm


class ProductPage(generic.ListView):
    """
    Class: ProductPage
    - Displays a list of products, filtered by category.
      The view retrieves all products or products from a specific category
      based on the 'category_slug'.

    Attributes:
    - model: The Product model that the view operates on.
    - template_name: The template to render, which is 'product_page.html'.
    - context_object_name: ('products') The name of the context variable
                           to be used in the template.

    Methods:
    - get_context_data: Adds additional context to the view, including:
      - A form for adding a product (AddProductForm).
      - A dictionary of products grouped by category.
      - A list of all categories.
    """

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
    """
    View: DeleteProduct
    - Handles the deletion of a product. When a product is deleted,
      the user is redirected back to the index page.

    Methods:
    - get: Handles the GET request, checks if the product exists, deletes it,
      and shows a success message.
      If the product does not exist, an error message is shown.
    """

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
    """
    View: product_detail
    - Displays the details of a specific product based on its slug.
      This view renders the 'product_detail.html' template with the
      selected product.
    """

    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


def add_product(request):
    """
    View: add_product
    - Handles the creation of a new product. The form includes options
      to add a product and its category. If the form is valid,
      the product is saved and the user is redirected to the index page.
      If invalid, an error message is displayed.

    Methods:
    - request.method == 'POST': Handles form submission.
    """

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
