from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View,
    FormView,
)
from django.db.models import Q
from .models import FoodItem

# Create your views here.


class MenuView(ListView):
    model = FoodItem
    template_name = "menu.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Include information about the signed-in user if authenticated

        return context


class FoodDetailsView(DetailView):
    model = FoodItem
    template_name = "food_details.html"
    fields = ("name", "price", "notes")
