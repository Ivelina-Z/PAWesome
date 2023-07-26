from django.contrib import admin

from PAWesome.adoption.models import AdoptionSurvey, SubmittedAdoptionSurvey
from PAWesome.animal.models import Animal


@admin.register(AdoptionSurvey)
class AdoptionSurveyAdmin(admin.ModelAdmin):

    def get_fields(self, request, *args, **kwargs):
        fields = super().get_fields(request, *args, **kwargs)
        if not request.user.is_superuser:
            fields.remove('created_by')
        return fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.organization
        return super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display = ('questionnaire_text', 'created_by') if request.user.is_superuser else ('__str__', 'questionnaire_text')
        return list_display


@admin.register(SubmittedAdoptionSurvey)
class SubmittedAdoptionFormAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'questionnaire_text')
