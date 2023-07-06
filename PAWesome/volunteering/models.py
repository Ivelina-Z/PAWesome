from django.db import models


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

