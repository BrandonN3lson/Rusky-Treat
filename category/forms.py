from django import forms
from .models import Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = {'title', 'description', 'featured_image', }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(

                'title',
                'description',
                'featured_image',
                ),

        self.helper.add_input(Submit('submit', 'Add Category'))
