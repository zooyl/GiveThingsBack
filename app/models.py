from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.name


class Foundation(models.Model):
    name = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=128, blank=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class GiveAway(models.Model):
    count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    bags = models.IntegerField(default=1)
    foundation = models.ForeignKey(Foundation, null=True, on_delete=models.SET_NULL)


class AdditionalInfo(models.Model):
    rules = models.CharField(max_length=1024)
    policy = models.CharField(max_length=1024)
    instruction = models.CharField(max_length=1024)


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    donation = models.ForeignKey(GiveAway, on_delete=models.CASCADE)

    street = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    postal = models.TextField(max_length=32, blank=True)
    phone = models.IntegerField(null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    details = models.TextField(max_length=256, blank=True)


class Gathering(models.Model):
    count = models.IntegerField(default=0)
    place = models.CharField(max_length=128)
    goal = models.CharField(max_length=128)
    needed = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    time = models.DateField()
    description = models.CharField(max_length=256)
    photo = models.ImageField(blank=True)
    person = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
