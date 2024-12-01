from django.views import generic
from .models import About


class AboutPage (generic.ListView):
    model = About
    template_name = "about.html"
    context_object_name = 'about'

    def get_queryset(self):
        return About.objects.prefetch_related('images')
