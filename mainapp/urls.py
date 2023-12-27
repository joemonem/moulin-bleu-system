from django.urls import path
from .views import (
    HomeView,
    CustomersView,
    AddCustomerView,
    CustomerDetailsView,
    EditCustomerView,
    CustomerSearchView,
    # orderDetailsView,
    # AddPostView,
    # UpdatePostView,
)


# urlpatterns = [path("", views.home, name="home")]
urlpatterns = [
    # path("", AboutView.as_view(), name="about"),
    path("", HomeView.as_view(), name="home"),
    path("customers", CustomersView.as_view(), name="customers"),
    path("add_customer", AddCustomerView.as_view(), name="add_customer"),
    path("customer/<int:pk>", CustomerDetailsView.as_view(), name="customer_details"),
    path("customer/edit/<int:pk>", EditCustomerView.as_view(), name="edit_customer"),
    path("customer/search", CustomerSearchView.as_view(), name="customer_search"),
    # path(
    #     "custom_login_redirect/",
    #     CustomLoginRedirectView.as_view(),
    #     name="custom_login_redirect",
    # ),
    # path(
    #     "search_redirect",
    #     SearchRedirectView.as_view(),
    #     name="search_redirect",
    # ),
    # path("addpost", AddPostView.as_view(), name="addpost"),
    # path("order/<int:pk>", OrderDetailsView.as_view(), name="order-details"),
    # path("order/edit/<int:pk>", UpdatePostView.as_view(), name="update_post"),
    # path("order/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
]
