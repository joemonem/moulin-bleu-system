from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Customer(models.Model):
    # Full name
    name = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=32)

    # Goole Plus Code location
    location = models.CharField(max_length=200, blank=True)

    # the date our customer was added to our database
    date_added = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name + " | " + str(self.phone_number)

    def get_absolute_url(self):
        return reverse("home")
