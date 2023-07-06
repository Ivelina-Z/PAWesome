from django.contrib import admin

from PAWesome.adoption.models import AdoptionSurvey, SubmittedAdoptionSurvey


@admin.register(AdoptionSurvey)
class AdoptionSurveyAdmin(admin.ModelAdmin):
    pass


@admin.register(SubmittedAdoptionSurvey)
class SubmittedAdoptionFormAdmin(admin.ModelAdmin):
    pass
