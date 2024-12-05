from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic, View
from django.contrib import messages
from .models import Category
from .forms import AddCategoryForm
from product.forms import AddProductForm


class IndexPage(generic.ListView):
    """
    IndexPage View.

    This class-based view displays the homepage of the
    Rusky Treats Django project.
    It lists all the available categories

    Attributes:
        model (Category): The model used to retrieve category data.
        template_name (str): The name of the template used to render the page.
        context_object_name (str): The context variable name for the category
        list.

    Methods:
        get_context_data(**kwargs): Adds `AddCategoryForm` and
                                    `AddProductForm` to
                                    the context data for use in the template.
    """
    model = Category
    template_name = "index.html"
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_category_form'] = AddCategoryForm()
        context['add_product_form'] = AddProductForm()

        # context['form'] = AddCategoryForm()
        return context


def add_category(request):
    """
    Add Category View.

    Handles the creation of a new category through a POST request.
    Validates the form data and saves the new category to the database.
    If the form is invalid, it renders
    the homepage with an error message.
    """

    if request.method == 'POST':
        add_category_form = AddCategoryForm(request.POST, request.FILES)
        if add_category_form.is_valid():
            add_category_form.save()
            return redirect('index')
        else:
            messages.error(request, 'form is invalid')
    return render(request, 'index.html',
                  {'add_category_form': add_category_form})


class DeleteCategory(View):
    """
    DeleteCategory View.

    Handles the deletion of a specific category based on its title.
    If the category exists, it is deleted, and a success message is displayed.
    If it does not exist, an error message is shown.
    """

    def get(self, request, category_title):
        try:
            category = get_object_or_404(Category, title=category_title)
        except Category.DoesNotExist:
            messages.error(request, 'Category doesnt exist')
            return redirect('index')
        category.delete()
        messages.success(request,
                         f'category {category_title} has been deleted')
        return redirect('index')
