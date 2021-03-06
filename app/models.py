from django.db import models
from django.contrib.auth.models import User


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
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    bags = models.IntegerField(default=1)
    foundation = models.ForeignKey(Foundation, null=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    archived = models.BooleanField(default=False)


class AdditionalInfo(models.Model):
    rules = models.CharField(max_length=1024)
    policy = models.CharField(max_length=1024)
    instruction = models.CharField(max_length=1024)


class SiteUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation = models.ForeignKey(GiveAway, on_delete=models.CASCADE)
    street = models.CharField(max_length=128, blank=False)
    city = models.CharField(max_length=128, blank=False)
    postal = models.TextField(max_length=32, blank=False)
    phone = models.IntegerField(null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=True)
    details = models.TextField(max_length=256, blank=True)


class Gathering(models.Model):
    place = models.CharField(max_length=128)
    goal = models.CharField(max_length=128)
    needed = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    time = models.DateField()
    description = models.CharField(max_length=256)
    person = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
