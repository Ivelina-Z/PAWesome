from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from PAWesome.animal.models import Animal
from PAWesome.organization.models import Organization


class AdoptionSurvey(models.Model):
    questionnaire_text = models.JSONField()

    created_by = models.OneToOneField(
        to=Organization,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Форма за осиновявaнe - {self.created_by}'


class SubmittedAdoptionSurvey(models.Model):
    STATUS_MAX_LENGTH = 8

    STATUS_CHOICES = [
        ('pending', 'Чакащ за одобрение'),
        ('approved', 'Одобрен'),
        ('rejected', ' Отхвърлен'),
    ]
    email = models.fields.EmailField(verbose_name='Имейл')

    phone_number = PhoneNumberField(verbose_name='Телефонен номер')

    questionnaire_text = models.JSONField()

    status = models.fields.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default='pending'
    )

    animal = models.ForeignKey(
        to=Animal,
        on_delete=models.CASCADE
    )

    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Adoption form from {self.email} for {self.animal}.'
