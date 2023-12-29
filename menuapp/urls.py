from django.urls import path
from .views import MenuView, FoodDetailsView, EditFoodView


urlpatterns = [
    path("menu", MenuView.as_view(), name="menu"),
    path("food_details/<int:pk>", FoodDetailsView.as_view(), name="food_details"),
    path("food_details/edit/<int:pk>", EditFoodView.as_view(), name="edit_food"),
]
