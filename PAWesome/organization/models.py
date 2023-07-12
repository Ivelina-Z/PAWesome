from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PAWesome.validators import FileSizeValidator

from phonenumber_field.modelfields import PhoneNumberField




class Organization(models.Model):
    name = models.fields.CharField(
        max_length=40,
        unique=True,
        verbose_name='Име'
    )

    phone_number = PhoneNumberField(verbose_name='Телефонен номер')

    email = models.fields.EmailField(
        verbose_name='Имейл'
    )

    description = models.fields.TextField(
        blank=True,
        verbose_name='Описание'
    )

    logo_image = models.ImageField(
        blank=True,
        validators=(FileSizeValidator(5), ),
        verbose_name='Лого'
    )

    slug = models.fields.SlugField(unique=True)

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.fields.CharField(max_length=30, verbose_name='Собствено име')
    last_name = models.fields.CharField(max_length=30, verbose_name='Фамилия')
    phone_number = PhoneNumberField(verbose_name='Телефонен номер')
    email = models.fields.EmailField(verbose_name='Имейл')
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
