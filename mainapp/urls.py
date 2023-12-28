from django.urls import path
from .views import (
    HomeView,
    CustomersView,
    AddCustomerView,
    CustomerDetailsView,
    EditCustomerView,
    CustomerSearchView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("customers", CustomersView.as_view(), name="customers"),
    path("add_customer", AddCustomerView.as_view(), name="add_customer"),
    path("customer/<int:pk>", CustomerDetailsView.as_view(), name="customer_details"),
    path("customer/edit/<int:pk>", EditCustomerView.as_view(), name="edit_customer"),
    path("customer/search", CustomerSearchView.as_view(), name="customer_search"),
]
