from django import forms
from django.db import models
from .models import Order, OrderItem
from django.forms import inlineformset_factory, formset_factory

from menuapp.models import FoodItem
from mainapp.models import Customer
from dal import autocomplete


class FoodItemQuantityForm(forms.Form):
    food_item = forms.ModelChoiceField(
        queryset=FoodItem.objects.all(),
        label="Food Item",
        widget=autocomplete.ModelSelect2(
            url="food-item-autocomplete", attrs={"data-minimum-input-length": 2}
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
                url="customer-autocomplete", attrs={"data-minimum-input-length": 2}
            ),
            "needed_for": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"}),
        }


FoodItemFormSet = formset_factory(FoodItemQuantityForm, extra=4, can_delete=True)


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()
