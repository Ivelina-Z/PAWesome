from django.urls import path

from PAWesome.adoption.views import AddAdoptionSurvey, AdoptForm, EditAdoptForm

urlpatterns = [
    path('adopt/<int:pk>', AdoptForm.as_view(), name='adopt-form'),
    path('organization/adoption-survey/add', AddAdoptionSurvey.as_view(), name='adopt-form-add'),
    path('organization/adoption-survey/edit', EditAdoptForm.as_view(), name='adopt-form-edit')
]
