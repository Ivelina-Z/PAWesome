import json
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from PAWesome.adoption.forms import AdoptionSurveyForm
from PAWesome.adoption.models import AdoptionSurvey, SubmittedAdoptionSurvey
from django.forms import formset_factory, CharField

from PAWesome.animal.models import Animal
from PAWesome.organization.models import Organization


# AdoptionSurveyFormSet = formset_factory(AdoptionSurveyForm, extra=1)


class AddAdoptionSurveyView(View):
    # model = AdoptionSurvey
    template_name = 'survey-add.html'

    # form_class = AdoptionSurveyFormSet
    # success_url = reverse_lazy('dashboard')
    # QuestionFormSet = formset_factory(AdoptionSurveyForm)

    def get(self, request, *args, **kwargs):
        AdoptionSurveyFormSet = formset_factory(AdoptionSurveyForm, extra=1)
        formset = AdoptionSurveyFormSet()
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, *args, **kwargs):
        AdoptionSurveyFormSet = formset_factory(AdoptionSurveyForm, extra=0)
        formset = AdoptionSurveyFormSet(request.POST, request.FILES)  # TODO: Try without FILES

        if formset.is_valid():
            data = {request.POST.get(f'form-{idx}-question'): '' for idx in range(formset.total_form_count())}
            AdoptionSurvey.objects.create(question_text=data, created_by_id=1)
            return redirect('homepage')

        return redirect('survey-add')


class AdoptFormView(CreateView):
    template_name = 'adopt-form.html'
    model = SubmittedAdoptionSurvey
    fields = []
    success_url = 'homepage'
    # form_class = AdoptForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        json_data = AdoptionSurvey.objects.get(created_by=1).questionnaire_text  # TODO: It' shouldn't be hardcoded

        for field_name, field_value in json_data.items():
            form.fields[field_name] = CharField(label=field_name, required=False, initial=field_value)
        return form

    def form_valid(self, form):
        json_form = json.dumps(form.cleaned_data)
        animal = Animal.objects.get(pk=self.kwargs['pk'])
        organization = Organization.objects.get(pk=1)
        form.instance.questionnaire_text = json_form
        form.instance.status = 'pending'
        form.instance.animal = animal
        form.instance.organization = organization

        return super().form_valid(form)

    # I have a created_by; Should return it when saved.
