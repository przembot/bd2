from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    type_choices = (
        ('C', 'Client'),
        ('E', 'Employee'),
    )
    user_type = models.CharField(max_length=1,
                                 choices=type_choices,
                                 default='C')
    birthdate = models.DateField()
    adress = models.CharField(max_length=100)

    # REQUIRED_FIELDS are added to fields when creating superuser
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email',
                       'birthdate', 'adress', 'user_type']


class Client(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                primary_key=True)


class Employee(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                primary_key=True)
    pesel = models.CharField(max_length=11,
                             unique=True)
