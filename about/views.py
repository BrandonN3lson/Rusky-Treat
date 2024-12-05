from django.views import generic
from .models import About


class AboutPage (generic.ListView):
    """
    Class:
    AboutPage View: A ListView that retrieves and renders the About Model
                    along with its associated Images

    Attributes:
                model: specifies About model as the data source
                template_name: specifies the template to render the About page
                context_object_anme: specifies the context variable name
                                     for the template
    Method:
    get_quertset: Customizes the queryset to prefetch related images.
    """

    model = About
    template_name = "about.html"
    context_object_name = 'about'

    def get_queryset(self):
        return About.objects.prefetch_related('images')
