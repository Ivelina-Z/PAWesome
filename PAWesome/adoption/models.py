from django.db import models

from PAWesome.animal.models import Animal
from PAWesome.organization.models import Organization


class AdoptionSurvey(models.Model):
    questionnaire_text = models.JSONField()

    created_by = models.OneToOneField(
        to=Organization,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'adoption survey - {self.created_by}'


class SubmittedAdoptionSurvey(models.Model):
    STATUS_MAX_LENGTH = 30
    STATUS_CHOICES = [
        ('pending', 'Чакащ за одобрение'),
        ('approved', 'Одобрен'),
        ('rejected', ' Отхвърлен'),
    ]

    questionnaire_text = models.JSONField()

    status = models.fields.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES
    )  # TODO: when status is changed to approved or rejected send mail.

    animal = models.ForeignKey(
        to=Animal,
        on_delete=models.CASCADE
    )

    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.CASCADE
    )
