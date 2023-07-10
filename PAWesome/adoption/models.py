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
    questionnaire_text = models.JSONField()

    STATUS_CHOICES = [
        ('pending', 'Waiting for approval'),
        ('approved', 'Approved')
    ]

    status = models.fields.CharField(max_length=30, choices=STATUS_CHOICES)
    animal = models.ForeignKey(to=Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)


