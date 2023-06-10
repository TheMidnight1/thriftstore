from django import forms
from .models import Product, Category, Condition, Comment

from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "condition",
            "name",
            "brand",
            "description",
            "price",
            "manufactured_date",
            "product_image",
            "quantity",
        ]
        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
                }
            ),
            "condition": forms.Select(
                attrs={
                    "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
                }
            ),
            "brand": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
                }
            ),
            "manufactured_date": forms.DateInput(
                attrs={
                    "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
                }
            ),
            "product_image": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
                }
            ),
        }


# class CommentForm(forms.Form):
#     content = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="Content")
    product_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update(
            {
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500"
            }
        )  #     product_id = forms.IntegerField(widget=forms.HiddenInput)
