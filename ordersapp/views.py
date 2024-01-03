from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy


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
from .forms import OrderItemForm, OrderItemFormSet, OrderForm


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


class AddOrderView(CreateView):
    model = Order
    template_name = "add_order.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders")

    def get_context_data(self, **kwargs):
        data = super(AddOrderView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["order_items"] = OrderItemFormSet(self.request.POST)
        else:
            data["order_items"] = OrderItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context["order_items"]

        with transaction.atomic():
            self.object = form.save()

            if order_items.is_valid():
                order_items.instance = self.object

                order_items.save()
        return super(AddOrderView, self).form_valid(form)

    def get_success_url(self):
        # Assuming your Order model has a many-to-many relationship with OrderItem
        # Update the order_items field of the Order instance with the newly created OrderItem instances
        order_items = OrderItem.objects.filter(order=self.object)
        self.object.order_items.set(order_items)

        return reverse("orders")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         context["order_items_formset"] = OrderItemFormSet(self.request.POST)
    #     else:
    #         context["order_items_formset"] = OrderItemFormSet()
    #     return context

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     order_items_formset = context["order_items_formset"]

    #     # Validate the formset
    #     if order_items_formset.is_valid():
    #         # Save the Order instance
    #         order = form.save()

    # # Associate the OrderItem instances with the Order
    # for order_item_form in order_items_formset:
    #     food_item = order_item_form.cleaned_data.get("food_item")
    #     quantity = order_item_form.cleaned_data.get("quantity")

    #     # Check if the entry already exists in OrderItem to avoid saving duplicates
    #     existing_order_item = OrderItem.objects.filter(
    #         food_item=food_item,
    #         quantity=quantity,
    #     ).first()

    #     if not existing_order_item:
    #         order_items_model = OrderItem(
    #             food_item=food_item, quantity=quantity, linked_order=order
    #         )
    #         order_items_model.save()
    #     else:
    #         order_items_model = existing_order_item

    #     order.order_items.add(order_items_model)

    # # Save the Order instance with the updated order_items
    # order.save()

    #         # Redirect to the success URL
    #         return super().form_valid(form)
    #     else:
    #         # If the formset is not valid, handle the error or redirect as needed
    #         # For example, you might want to return HttpResponseBadRequest
    #         return self.form_invalid(form)


class OrderSearchView(TemplateView):
    model = Order
    template_name = "order_search.html"

    def post(self, request, *args, **kwargs):
        # Access search query from POST data
        customer = request.POST.get("submission")

        # Perform case-insensitive search on customer name
        customer_orders = Order.objects.filter(
            customer__name__icontains=customer
        ).order_by(  # Sorts them from latest "created_at" date
            "-created_at"
        )

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
