from django.db import models
from menuapp.models import FoodItem
from mainapp.models import Customer
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.


# One order item, includes one food item alongside its quantity.
class OrderItem(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    # Need to accept floats mosly for the items sold in dozens like sambousek (half dozen, dozen and a half...)
    quantity = models.FloatField()

    @property
    def price(self):
        return self.food_item.price * self.quantity

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"


# One order item, includes one food item alongside its quantity.
class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=False, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    needed_for = models.DateTimeField()
    order_items = models.ManyToManyField(OrderItem, null=False)
    paid = models.BooleanField(null=False, default=False)
    delivery = models.BooleanField(null=False, default=False)
    notes = models.TextField(null=True)

    def calculate_total_price(self):
        self.total_price = sum(item.price for item in self.order_items.all())
        self.save()

    @property
    def total_price(self):
        return sum(item.price for item in self.order_items.all())

    def __str__(self):
        return f"{self.customer.name} -- ${self.total_price} -- paid: {self.paid} -- needed for: {self.needed_for}"
