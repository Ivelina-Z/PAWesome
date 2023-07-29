from django.urls import path

from PAWesome.adoption.views import AddAdoptionForm, SubmitAdoptForm, EditAdoptForm

urlpatterns = [
    path('adopt/<int:pk>', SubmitAdoptForm.as_view(), name='submit-adopt-form'),
    path('organization/adoption-survey/add', AddAdoptionForm.as_view(), name='adopt-form-add'),
    path('organization/adoption-survey/edit', EditAdoptForm.as_view(), name='adopt-form-edit')
]
