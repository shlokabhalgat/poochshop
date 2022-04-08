from django.db import models
from djongo import models
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from mongoengine import Document
from mongoengine.fields import (FloatField, IntField,
                                StringField,
                                ListField,
                                URLField,
                                ObjectIdField,
                                BooleanField,
                                DateField)

# Create your models here.

AMOUNT_CHOICES = [
    ('LT100', 'less than 1000'),
    ('BET1000TO3000', '₹1000-₹3000'),
    ('BET3000TO5000', '₹3000-₹5000'),
    ('MT500', 'more than ₹5000')
]

SERVICE_CHOICES = [
    ('pet_grooming', 'Pet Grooming'),
    ('pet_sitting', 'Pet Sitting'), ('vet', 'Vet/At home vet'), ('pet_hostel', 'Pet hostel'),
    ('food_delivery', 'Home-made food delivery'),
    ('pet_taxi', 'Pet Taxi'), ('pet_party', 'Pet Party')
]


class PetFormData(models.Model):
    abstract = True
    index = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    amount_spent = models.CharField(max_length=100, choices=AMOUNT_CHOICES)
    pincode = models.CharField(max_length=15)
    services_required = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    auth_user_email = models.ForeignKey(User, on_delete=models.CASCADE)


class VendorData(Document):
    meta = {'collection': 'vendors'}
    ID = ObjectIdField()
    Category = StringField()
    VendorName = StringField()
    Socials = StringField()
    WaysOfBooking = StringField()
    PhoneNumber = StringField()
    Email = StringField()
    Address = StringField()
    Pincode = StringField()
    City = StringField()
    Services = StringField()
    Charges = StringField()
    DailyNumberOfCustomers = StringField()
    PetCategory = StringField()


class MongoPetData(Document):
    meta = {'collection': 'poochshop_apps_petformdata'}
    index = IntField()
    name = StringField()
    age = IntField()
    breed = StringField()
    amount_spent = StringField()
    pincode = StringField()
    services_required = StringField()
    auth_user_email_id = IntField()


# class AuthUser(Document):
#     meta = {'collection': 'auth_user'}
#     _id = IntField()
#     id = IntField()
#     password = StringField()
#     last_login = DateField()
#     is_superuser = BooleanField()
#     username = StringField()
#     first_name = StringField()
#     last_name = StringField()
#     email = StringField()
#     is_staff = BooleanField()
#     is_active = BooleanField()
#     dat_joined = DateField()
