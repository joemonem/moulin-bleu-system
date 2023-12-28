from django.urls import path
from .views import MenuView, FoodDetailsView


urlpatterns = [
    path("menu", MenuView.as_view(), name="menu"),
    path("food_details/<int:pk>", FoodDetailsView.as_view(), name="food_details"),
]
