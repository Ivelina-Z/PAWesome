from django.contrib.auth import get_user_model
from django.db import models
from PAWesome.validators import FileSizeValidator

from phonenumber_field.modelfields import PhoneNumberField

UserModel = get_user_model()


class Organization(models.Model):
    NAME_MAX_LENGTH = 40
    LOGO_MAX_FILE_SIZE = 5

    name = models.fields.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Име'
    )

    phone_number = PhoneNumberField(
        verbose_name='Телефонен номер'
    )

    email = models.fields.EmailField(
        verbose_name='Имейл'
    )

    description = models.fields.TextField(
        blank=True,
        verbose_name='Описание'
    )

    logo_image = models.ImageField(
        blank=True,
        validators=(FileSizeValidator(LOGO_MAX_FILE_SIZE), ),
        verbose_name='Лого',
        upload_to='images/'
    )

    slug = models.fields.SlugField(unique=True)

    user = models.OneToOneField(to=UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Employee(models.Model):
    NAME_MAX_LENGTH = 30

    first_name = models.fields.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Собствено име'
    )

    last_name = models.fields.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Фамилия'
    )

    phone_number = PhoneNumberField(
        verbose_name='Телефонен номер'
    )

    email = models.fields.EmailField(
        verbose_name='Имейл'
    )

    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)

    user = models.OneToOneField(to=UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
