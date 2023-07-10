from django.urls import path

from PAWesome.adoption.views import AddAdoptionSurveyView, AdoptFormView

urlpatterns = [
    path('adopt/<int:pk>', AdoptFormView.as_view(), name='adopt-form'),
    path('organization/adoption-survey/add', AddAdoptionSurveyView.as_view(), name='adopt-form-add')
    # path('organization/adoption-old-survey/add', create_survey, name='survey-add')
]