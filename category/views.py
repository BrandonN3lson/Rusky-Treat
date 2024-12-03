from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic, View
from django.contrib import messages
from .models import Category
from .forms import AddCategoryForm
from product.forms import AddProductForm


class IndexPage(generic.ListView):
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
