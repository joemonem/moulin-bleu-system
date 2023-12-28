from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class FoodItem(models.Model):
    # Food item's name
    name = models.CharField(max_length=255)

    price = models.IntegerField()

    # Notes about the food item. e.g: ingredtients, heating method, storage method
    notes = models.TextField()

    def __str__(self):
        return self.name + " | " + str(self.price)

    def get_absolute_url(self):
        return reverse("home")
