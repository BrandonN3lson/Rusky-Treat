"""About app admin config."""

from django.contrib import admin
from .models import About, AboutImages
from django_summernote.admin import SummernoteModelAdmin


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    """Admin configuration for the About app."""

    summernote_fields = ('content',)


admin.site.register(AboutImages)
