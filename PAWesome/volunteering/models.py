from django.db import models
from django.contrib.gis.db import models as gis_model
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField

from PAWesome.organization.models import Organization


class FosterHome(models.Model):
    phone_number = PhoneNumberField(
        verbose_name='Телефонен номер'
    )

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

    additional_info = models.fields.TextField(
        blank=True,
        null=True,
        verbose_name='Допълнителна информация'
    )

    location = gis_model.PointField(
        verbose_name='Местоположение'
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


class DonationTickets(models.Model):
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
