from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy
from dal import autocomplete
from mainapp.models import Customer
from menuapp.models import FoodItem

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
from django.db import transaction
from .models import OrderItem, Order
from django.utils import timezone
from .forms import OrderItemForm, OrderForm, FoodItemFormSet


# Create your views here.


class OrderItemsView(ListView):
    model = OrderItem
    template_name = "order_items.html"
    context_object_name = "order_items"


class OrdersView(ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    ordering = ["-created_at"]


class OrderDetailsView(DetailView):
    model = Order
    template_name = "order_details.html"
    fields = "__all__"

    def post(self, request, pk):
        order_item = get_object_or_404(Order, pk=pk)

        # Toggle plat_du_jour value
        order_item.paid = not order_item.paid
        order_item.save()  # Save the change to the database

        # ... redirect or handle success ...
        return redirect("order_details", pk=pk)


class EditOrderView(UpdateView):
    model = Order
    template_name = "edit_order.html"
    form_class = OrderForm
    # fields = ("order_items", "needed_for", "paid")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the order being edited
        order = self.object

        # Pass the instance to the OrderForm to display existing data
        context["order_form"] = OrderForm(instance=order)

        # Pass the initial values for the FoodItemFormSet based on the existing order items
        food_items_initial = [
            {"food_item": item.food_item, "quantity": item.quantity}
            for item in order.order_items.all()
        ]
        context["food_item_formset"] = FoodItemFormSet(
            prefix="food_items", initial=food_items_initial
        )

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        new_order = self.object
        # Clear existing order items
        new_order.order_items.clear()

        # Access food item formset
        food_item_formset = FoodItemFormSet(self.request.POST, prefix="food_items")

        # Accessing values of food_item and quantity from the form
        for food_form in food_item_formset:
            # Checking its validity is essential
            if food_form.is_valid():
                food_item = food_form.cleaned_data["food_item"]
                quantity = food_form.cleaned_data["quantity"]

                # Check if that Order Item exists to avoid creating duplicates
                existing_order_item = OrderItem.objects.filter(
                    food_item=food_item,
                    quantity=quantity,
                ).first()

                if existing_order_item:
                    # Use the existing OrderItem if it exists
                    new_order_item = existing_order_item
                else:
                    # Create a new OrderItem if it doesn't exist
                    new_order_item = OrderItem(food_item=food_item, quantity=quantity)
                    new_order_item.save()

                new_order.order_items.add(new_order_item)

        # Continue with the default form_valid behavior
        return response

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


class AddOrderView(CreateView):
    model = Order
    template_name = "add_order.html"
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_form"] = OrderForm()
        context["food_item_formset"] = FoodItemFormSet(prefix="food_items")
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        new_order = self.object

        # Access food item formset
        food_item_formset = FoodItemFormSet(self.request.POST, prefix="food_items")

        # Accessing values of food_item and quantity from the form
        for food_form in food_item_formset:
            # Checking its validity is essential
            if food_form.is_valid():
                food_item = food_form.cleaned_data["food_item"]
                quantity = food_form.cleaned_data["quantity"]

                # Check if that Order Item exists to avoid creating duplicates
                existing_order_item = OrderItem.objects.filter(
                    food_item=food_item,
                    quantity=quantity,
                ).first()

                if existing_order_item:
                    # Use the existing OrderItem if it exists
                    new_order_item = existing_order_item
                else:
                    # Create a new OrderItem if it doesn't exist
                    new_order_item = OrderItem(food_item=food_item, quantity=quantity)
                    new_order_item.save()

                new_order.order_items.add(new_order_item)

        # Continue with the default form_valid behavior
        return response

    def get_success_url(self):
        order = self.object.pk
        return reverse("order_details", args=[order])


class CustomerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Customer.objects.all()

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) | Q(phone_number__icontains=self.q)
            )

        return qs


class FoodItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = FoodItem.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class OrderSearchView(TemplateView):
    model = Order
    template_name = "order_search.html"

    def post(self, request, *args, **kwargs):
        # Access search query from POST data
        customer = request.POST.get("submission")

        if customer.isnumeric():
            # Customer is a number, search for order number
            customer_orders = Order.objects.filter(pk=int(customer)).order_by(
                "-created_at"
            )
        else:
            # Customer is a string, search for customer name
            customer_orders = Order.objects.filter(
                customer__name__icontains=customer
            ).order_by("-created_at")

        # Add food items to context
        context = self.get_context_data(**kwargs)
        context["customer_orders"] = customer_orders

        # User's submission
        context["customer"] = customer

        # Return the rendered template with context
        return self.render_to_response(context)


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
        future_pickup_orders = Order.objects.filter(
            needed_for__date__gt=today, delivery=False
        ).order_by(
            "needed_for"
        )  # Ordered by latest "needed_for" dates

        future_delivery_orders = Order.objects.filter(
            needed_for__date__gt=today, delivery=True
        ).order_by(
            "needed_for"
        )  # Ordered by latest "needed_for" dates

        context["future_pickup_orders"] = future_pickup_orders
        context["future_delivery_orders"] = future_delivery_orders

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
