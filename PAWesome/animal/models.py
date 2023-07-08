from django.db import models
from django.contrib.gis.db import models as gis_models

from PAWesome.organization.models import Organization
from PAWesome.validators import FileSizeValidator


class Animal(models.Model):
    name = models.fields.CharField(
        max_length=20,
        verbose_name='Име'
    )


    ANIMAL_TYPES = [
        ('cat', 'Коте'),
        ('dog', 'Куче'),
        ('bunny', 'Зайче')
    ]
    animal_type = models.fields.CharField(
        max_length=5,
        choices=ANIMAL_TYPES,
        verbose_name='Вид'
    )

    GENDER_CHOICES = [
        ('male', 'Мъжко'),
        ('female', 'Женско'),
        ('unknown', 'Неизвестен')
    ]
    gender = models.fields.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='Пол'
    )

    sprayed = models.fields.BooleanField(
        blank=True,
        null=True,
        verbose_name='Кастриран/а'
    )  # allows unknown

    vaccinated = models.fields.BooleanField(
        blank=True,
        null=True,
        verbose_name='Ваксиниран/а'
    )  # allows unknown
    medical_issues = models.fields.TextField(
        blank=True,
        verbose_name='Медицински проблеми'
    )

    description = models.fields.TextField(
        blank=True,
        verbose_name='Описание'
    )

    RESIDENCE_CHOICES = [
        ('vet', 'Ветеринарна клиника'),
        ('home', 'Приемен дом'),
        ('street', 'На улицата')
    ]
    current_residence = models.fields.CharField(
        max_length=30,
        choices=RESIDENCE_CHOICES,
        verbose_name='Настанен в'
    )

    # TODO: Foster home - PROBLEMATIC
    # foster_home = models.OneToOneField(to=FosterHomes, on_delete=models.PROTECT, blank=True, null = True)
    # # I want it to not be able to delete a foster home if animals in it

    vet = models.fields.CharField(
        max_length=40,
        blank=True,
        verbose_name='Ветеринарна клиника'
    )

    location = gis_models.PointField()

    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    date_of_publication = models.fields.DateField(auto_now_add=True)
    # slug = models.fields.SlugField(unique=True)

    def __str__(self):
        return f'{self.animal_type} {self.name}'


class AnimalPhotos(models.Model):
    animal = models.ForeignKey(
        to=Animal,
        on_delete=models.CASCADE,
        related_name='photos'
    )

    # photo = models.URLField()

    photo = models.ImageField(
        blank=True,
        null=True,
        validators=(FileSizeValidator(5),),
        upload_to='images/'
    )

    is_main_image = models.BooleanField()

    def __str__(self):
        return f'{self.animal} main photo' if self.is_main_image else f'{self.animal} photo'
