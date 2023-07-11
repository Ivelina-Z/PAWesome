from django.db import models
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField

from PAWesome.organization.models import Organization


class FosterHome(models.Model):
    location = models.fields.CharField(
        max_length = 30,
        verbose_name='Местоположение'
    )  # TODO: Change to drop down with options; implement django smart select

    phone_number = models.fields.CharField(
        max_length=11,
        verbose_name='Телефонен номер'
    )  # TODO: Regex Validator drop down menu with country options and codes

    cat_available_spots = models.fields.IntegerField(
        blank=True,
        null=True,
        verbose_name='Брой места за котета'
    )

    dog_available_spots = models.fields.IntegerField(
        blank=True,
        null=True,
        verbose_name='Брой места за кучета'
    )

    bunny_available_spots = models.fields.IntegerField(
        blank=True,
        null=True,
        verbose_name='Брой места за зайчета'
    )


class DonationsDeliveryInfo(models.Model):
    name = models.fields.CharField(
        max_length=100,
        verbose_name='Имена на получател'
    )

    DELIVERY_TYPE_CHOICES = [
        ('office', 'до офис'),
        ('adress', 'до адрес')
    ]
    delivery_type = models.CharField(
        max_length=20,
        choices=DELIVERY_TYPE_CHOICES,
        verbose_name='Тип доставка')

    address = models.fields.CharField(
        max_length=200,
        verbose_name='Адрес за доставка'
    )

    phone_number = PhoneNumberField(
         verbose_name='Телефонен номер'
    )

    additional_info = models.fields.TextField(
        blank=True,
        verbose_name='Допълнителна информация'
    )

    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f'Доставка {self.get_delivery_type_display()} {self.address}'


class FoodDonationTickets(models.Model):
    item = models.fields.CharField(max_length=60)
    weight_quantity = models.fields.FloatField(
        blank=True,
        null=True,
        validators=(MinValueValidator(0),)
    )
    count_quantity = models.fields.IntegerField(
        blank=True,
        null=True,
        validators=(MinValueValidator(0),)
    )
    delivery_info = models.ManyToManyField(to=DonationsDeliveryInfo)
    created_by = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
