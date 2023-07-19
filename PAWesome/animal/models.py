
from django.db import models
from django.contrib.gis.db import models as gis_models

from PAWesome.organization.models import Organization
from PAWesome.validators import FileSizeValidator
from PAWesome.volunteering.models import FosterHome


class AnimalBase(models.Model):
    NAME_MAX_LENGTH = 20
    ANIMAL_TYPE_MAX_LENGTH = 5
    ANIMAL_TYPES = [
        ('cat', 'Коте'),
        ('dog', 'Куче'),
        ('bunny', 'Зайче')
    ]
    GENDER_MAX_LENGTH = 10
    GENDER_CHOICES = [
        ('male', 'Мъжко'),
        ('female', 'Женско'),
        ('unknown', 'Неизвестен')
    ]
    RESIDENCE_MAX_LENGTH = 30
    RESIDENCE_CHOICES = [
        ('vet', 'Ветеринарна клиника'),
        ('home', 'Приемен дом'),
        ('street', 'На улицата')
    ]
    VET_MAX_LENGTH = 40

    class Meta:
        abstract = True

    name = models.fields.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Име'
    )

    animal_type = models.fields.CharField(
        max_length=ANIMAL_TYPE_MAX_LENGTH,
        choices=ANIMAL_TYPES,
        verbose_name='Вид'
    )

    gender = models.fields.CharField(
        max_length=GENDER_MAX_LENGTH,
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

    current_residence = models.fields.CharField(
        max_length=RESIDENCE_MAX_LENGTH,
        choices=RESIDENCE_CHOICES,
        verbose_name='Настанен в'
    )

    # TODO: Make validator that checks if current residence - vet that vet is not blank, respectively for foster home
    foster_home = models.ForeignKey(
        to=FosterHome,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    vet = models.fields.CharField(
        max_length=VET_MAX_LENGTH,
        blank=True,
        verbose_name='Ветеринарна клиника'
    )

    location = gis_models.PointField()

    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    date_of_publication = models.fields.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.animal_type} {self.name}'


class Animal(AnimalBase):
    pass


class AnimalPhotos(models.Model):
    MAX_PHOTO_SIZE = 5

    animal = models.ForeignKey(
        to=Animal,
        on_delete=models.CASCADE,
        # related_name='photos'
    )

    photo = models.ImageField(
        blank=True,
        null=True,
        validators=(FileSizeValidator(MAX_PHOTO_SIZE), ),
        upload_to='images/',
    )

    is_main_image = models.BooleanField()

    def __str__(self):
        return f'{self.animal} main photo' if self.is_main_image else f'{self.animal} photo'


class AdoptedAnimalsArchive(AnimalBase):
    filled_questionnaire_text = models.JSONField()
    date_of_adoption = models.fields.DateField(auto_now_add=True)

