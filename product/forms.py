from django import forms
from .models import Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class AddProductForm(forms.ModelForm):
    """
    Class: AddProductForm
    - A form that provides a user interface for adding or editing
      `Product` objects.
      Uses `ModelForm` to create a form based on the `Product`
      model and uses `crispy-forms` to style the form fields.

    Attributes:
    - Meta:
        - model: Specifies the model this form is associated with (`Product`).
        - fields: A tuple of the fields to include in the form
                  (`category`, `name`, `description`, `price`, `image`).

    Methods:
    - __init__: Initializes the form and sets up custom styling and
                layout using `crispy-forms`.
      - `self.helper`: configures the form layout and includes the
                       submit button.

    """

    class Meta:
        model = Product
        fields = {'category', 'name', 'description', 'price', 'image', }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(

                'category',
                'name',
                'description',
                'price',
                'image',
                ),

        self.helper.add_input(Submit('submit', 'Add Product'))
