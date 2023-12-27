from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Customer(models.Model):
    # Full name
    name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=255)

    # what3words location
    location = models.CharField(max_length=255)

    # the date our customer was added to our database
    date_added = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name + " | " + str(self.phone_number)

    def get_absolute_url(self):
        return reverse("home")
