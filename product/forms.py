from django import forms
from .models import Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class AddProductForm(forms.ModelForm):
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
