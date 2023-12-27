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


from .models import Customer

# from .forms import PostForm, EditForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy, resolve
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.


class HomeView(ListView):
    model = Customer
    template_name = "home.html"
    context_object_name = "posts"

    # ordering = ["-published_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Include information about the signed-in user if authenticated

        return context


class CustomersView(ListView):
    model = Customer
    template_name = "customers.html"
    context_object_name = "customers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customers = Customer.objects.all()

        context["customers"] = customers

        return context


class AddCustomerView(CreateView):
    model = Customer
    template_name = "add_customer.html"
    # form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    # fields = "__all__"
    fields = ("name", "phone_number", "location")


class CustomerDetailsView(DetailView):
    model = Customer
    template_name = "customer_details.html"
    fields = ("name", "phone_number", "location", "date_added")


class EditCustomerView(UpdateView):
    model = Customer
    template_name = "edit_customer.html"
    fields = ("name", "phone_number", "location")

    # form_class = EditForm

    def get_success_url(self):
        username = self.request.user.username
        customer = self.object.pk
        return reverse("customer_details", args=[customer])


class CustomerSearchView(TemplateView):
    model = Customer
    template_name = "customer_search.html"

    def post(self, request, *args, **kwargs):
        # Access search query from POST data
        name_or_num = request.POST.get("submission")

        # Perform case-insensitive search on name and phone number
        customers = Customer.objects.filter(
            Q(name__icontains=name_or_num) | Q(phone_number__icontains=name_or_num)
        )

        # Add customers to context
        context = self.get_context_data(**kwargs)
        context["customers"] = customers

        # Return the rendered template with context
        return self.render_to_response(context)


# class TodaysOrderView(ListView):
#     model = Customer
#     template_name = "home.html"
#     context_object_name = "posts"

#     # ordering = ["-published_date"]

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Include information about the signed-in user if authenticated

#         return context