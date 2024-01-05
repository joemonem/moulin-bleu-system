from django import forms
from django.db import models
from .models import Order, OrderItem
from django.forms import inlineformset_factory, formset_factory

from menuapp.models import FoodItem
from mainapp.models import Customer
from dal import autocomplete


# I could use a form that has all the required fields for the Order model, and ditch the OrderItem model.
# class OrderForm(forms.Form):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
#     # Need to accept floats mosly for the items sold in dozens like sambousek (half dozen, dozen and a half...)
#     quantity = models.FloatField()


# class OrderItemForm(forms.ModelForm):
#     class Meta:
#         model = OrderItem
#         fields = ["food_item", "quantity"]


# OrderItemFormSet = inlineformset_factory(
#     Order,
#     OrderItem,
#     form=OrderItemForm,
#     extra=1,
# )


class FoodItemQuantityForm(forms.Form):
    food_item = forms.ModelChoiceField(
        queryset=FoodItem.objects.all(),
        label="Food Item",
        widget=autocomplete.ModelSelect2(
            url="food-item-autocomplete", attrs={"data-minimum-input-length": 3}
        ),
        empty_label="Select a food item",
    )
    quantity = forms.FloatField(label="Quantity", initial=1, min_value=0.5)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer",
            "needed_for",
            "paid",
            "delivery",
            "notes",
        ]

        widgets = {
            "customer": autocomplete.ModelSelect2(
                url="customer-autocomplete", attrs={"data-minimum-input-length": 3}
            ),
            "needed_for": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"}),
        }


FoodItemFormSet = formset_factory(FoodItemQuantityForm, extra=4, can_delete=True)


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()
