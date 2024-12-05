from django import forms
from .models import Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset


class AddCategoryForm(forms.ModelForm):
    """
    Class:
        AddCategoryForm:

        A ModelForm for creating new category instances
        including fields for title, description and featured_image

    Attributes:
        Meta:
            model: specifies the category model for the form
            field: defines the fields to include in the form

    Methods:
        __init__:
            Customizes the form initialization to set up Crispy Forms helper,
            define the form layout, and add a submit button.

    """
    class Meta:
        model = Category
        fields = {'title', 'description', 'featured_image', }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                'title',
                'description',
                'featured_image',
                )
        )

        self.helper.add_input(Submit('submit', 'Add Category'))
