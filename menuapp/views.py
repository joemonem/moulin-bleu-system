from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse


from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    TemplateView,
)
from django.db.models import Q
from .models import FoodItem

# Create your views here.


class MenuView(ListView):
    model = FoodItem
    template_name = "menu.html"
    context_object_name = "food_items"


class FoodDetailsView(DetailView):
    model = FoodItem
    template_name = "food_details.html"
    fields = ("name", "price", "notes")

    def post(self, request, pk):
        food_item = get_object_or_404(FoodItem, pk=pk)
        # ... handle other form data ...

        # Toggle plat_du_jour value
        food_item.plat_du_jour = not food_item.plat_du_jour
        food_item.save()  # Save the change to the database

        # ... redirect or handle success ...
        return redirect("food_details", pk=pk)


class EditFoodView(UpdateView):
    model = FoodItem
    template_name = "edit_food.html"
    fields = ("name", "price", "notes")

    def get_success_url(self):
        food_item = self.object.pk
        return reverse("food_details", args=[food_item])


class MenuSearchView(TemplateView):
    model = FoodItem
    template_name = "menu_search.html"

    def post(self, request, *args, **kwargs):
        # Access search query from POST data
        name = request.POST.get("submission")

        # Perform case-insensitive search on name
        food_items = FoodItem.objects.filter(name__icontains=name)

        # Add food items to context
        context = self.get_context_data(**kwargs)
        context["food_items"] = food_items

        # User's submission
        context["name"] = name

        # Return the rendered template with context
        return self.render_to_response(context)
