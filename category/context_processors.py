from .models import Category


def categories_context(request):
    """
    Context processor for including categories in templates.

    This function adds all category object to the context,
    making them accessible in any template where
    the context processor is enabled.
    """
    return {
        'categories': Category.objects.all()
    }
