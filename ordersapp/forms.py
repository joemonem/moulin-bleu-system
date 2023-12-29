from django import forms
from django.db import models
from menuapp.models import FoodItem
from mainapp.models import Customer
from .models import Order, OrderItem


# I could use a form that has all the required fields for the Order model, and ditch the OrderItem model.
class OrderForm(forms.Form):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    # Need to accept floats mosly for the items sold in dozens like sambousek (half dozen, dozen and a half...)
    quantity = models.FloatField()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("customer", "created_at", "order_items", "total_price")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "value": "",
                    "id": "authorField",
                    "type": "hidden",
                }
            ),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }
