from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, blank=False)


class Foundation(models.Model):
    name = models.CharField(max_length=128, blank=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)


class GiveAway(models.Model):
    count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    bags = models.IntegerField(default=1)
    foundation = models.ForeignKey(Foundation, on_delete=models.DO_NOTHING)


class Gathering(models.Model):
    count = models.IntegerField(default=0)
    place = models.CharField(max_length=128)
    goal = models.CharField(max_length=128)
    needed = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    time = models.DateField()
    description = models.CharField(max_length=256)
    photo = models.ImageField(blank=True)


class Delivery(models.Model):
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    postal = models.TextField(max_length=32)
    phone = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    details = models.TextField(max_length=256)


class AdditionalInfo(models.Model):
    rules = models.CharField(max_length=1024)
    policy = models.CharField(max_length=1024)
    instruction = models.CharField(max_length=1024)


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    donation = models.ForeignKey(GiveAway, on_delete=models.CASCADE)
    gathering = models.ForeignKey(Gathering, on_delete=models.CASCADE)
