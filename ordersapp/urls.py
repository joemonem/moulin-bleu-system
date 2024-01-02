from django.urls import path
from .views import (
    OrderItemsView,
    AddOrderItemView,
    OrdersView,
    OrderDetailsView,
    EditOrderView,
    FutureOrdersView,
    TodaysOrdersView,
    AddOrderView,
    OrderSearchView,
)


urlpatterns = [
    path("order_items", OrderItemsView.as_view(), name="order_items"),
    path("orders", OrdersView.as_view(), name="orders"),
    path("add_order_item", AddOrderItemView.as_view(), name="add_order_item"),
    path("add_order", AddOrderView.as_view(), name="add_order"),
    path("orders/<int:pk>", OrderDetailsView.as_view(), name="order_details"),
    path("orders/edit/<int:pk>", EditOrderView.as_view(), name="edit_order"),
    path("future_orders", FutureOrdersView.as_view(), name="future_orders"),
    path("todays_orders", TodaysOrdersView.as_view(), name="todays_orders"),
    path("order/search", OrderSearchView.as_view(), name="order_search"),
    # path("food_details/<int:pk>", FoodDetailsView.as_view(), name="food_details"),
    # path("food_details/edit/<int:pk>", EditFoodView.as_view(), name="edit_food"),
    # path("menu/search", MenuSearchView.as_view(), name="menu_search"),
]
