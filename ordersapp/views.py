from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse


from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View,
)
from django.db.models import Q
from .models import OrderItem, Order
from django.utils import timezone


# Create your views here.


class OrderItemsView(ListView):
    model = OrderItem
    template_name = "order_items.html"
    context_object_name = "order_items"


class OrdersView(ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"


class OrderDetailsView(DetailView):
    model = Order
    template_name = "order_details.html"
    fields = "__all__"


class EditOrderView(UpdateView):
    model = Order
    template_name = "edit_order.html"
    fields = ("order_items", "needed_for", "paid")

    # form_class = EditForm

    def get_success_url(self):
        order = self.object.pk
        return reverse("order_details", args=[order])


class FoodDetailsView(DetailView):
    model = OrderItem
    template_name = "food_details.html"
    fields = ("name", "price", "notes")

    def post(self, request, pk):
        food_item = get_object_or_404(OrderItem, pk=pk)
        # ... handle other form data ...

        # Toggle plat_du_jour value
        food_item.plat_du_jour = not food_item.plat_du_jour
        food_item.save()  # Save the change to the database

        # ... redirect or handle success ...
        return redirect("food_details", pk=pk)


class AddOrderItemView(CreateView):
    model = OrderItem
    template_name = "add_order_item.html"

    def get_success_url(self):
        return reverse("order_items")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    fields = "__all__"


class FutureOrdersView(ListView):
    model = Order
    template_name = "future_orders.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        # __gt means greater than, so we keep the orders needed for the future
        future_orders = Order.objects.filter(needed_for__date__gt=today)

        context["future_orders"] = future_orders

        return context


class TodaysOrdersView(ListView):
    model = Order
    template_name = "todays_orders.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        todays_orders = Order.objects.filter(needed_for__date=today)
        context["todays_orders"] = todays_orders

        return context
