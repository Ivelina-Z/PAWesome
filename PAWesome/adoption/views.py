import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, UpdateView

from PAWesome.adoption.forms import AdoptionSurveyForm
from PAWesome.adoption.models import AdoptionSurvey, SubmittedAdoptionSurvey
from django.forms import formset_factory, CharField

from PAWesome.animal.models import Animal
from PAWesome.organization.models import Organization


# AdoptionSurveyFormSet = formset_factory(AdoptionSurveyForm, extra=1)


class AddAdoptionSurveyView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'adopt-form-add.html'

    def get(self, request, *args, **kwargs):
        AdoptionSurveyFormSet = formset_factory(AdoptionSurveyForm, extra=0)
        formset = AdoptionSurveyFormSet(initial=[{'question': 'Име, Презиме, Фамилия'}, {'question': 'Телефон за контакт'}])
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, *args, **kwargs):
        AdoptionSurveyFormSet = formset_factory(AdoptionSurveyForm, extra=0)
        formset = AdoptionSurveyFormSet(request.POST, request.FILES)  # TODO: Try without FILES

        if formset.is_valid():
            data = {request.POST.get(f'form-{idx}-question'): '' for idx in range(formset.total_form_count())}
            AdoptionSurvey.objects.create(questionnaire_text=data, created_by_id=request.user.organization.pk)
            return redirect(reverse_lazy('dashboard', kwargs={'pk': self.request.user.organization.pk}))

        return redirect('survey-add')


class AdoptFormView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'adopt-form.html'
    model = SubmittedAdoptionSurvey
    fields = []
    success_url = 'homepage'
    # form_class = AdoptForm

    def get_form(self, form_class=None):
        animal = get_object_or_404(Animal, pk=self.kwargs['pk'])
        form = super().get_form(form_class)
        json_data = AdoptionSurvey.objects.get(created_by=animal.organization).questionnaire_text

        for field_name, field_value in json_data.items():
            form.fields[field_name] = CharField(label=field_name, required=False, initial=field_value)
        return form

    def form_valid(self, form):
        json_form = form.cleaned_data
        animal = get_object_or_404(Animal, pk=self.kwargs['pk'])
        organization = get_object_or_404(Organization, pk=animal.organization.pk)
        form.instance.questionnaire_text = json_form
        form.instance.status = 'pending'
        form.instance.animal = animal
        form.instance.organization = organization
        return super().form_valid(form)

    # I have a created_by; Should return it when saved.


class EditAdoptFormView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'adopt-form-edit.html'

    AdoptionSurveyFormSet = formset_factory(AdoptionSurveyForm, extra=0)

    def get(self, request, *args, **kwargs):
        organization = Organization.objects.get(pk=self.request.user.organization.pk)
        questions = get_object_or_404(AdoptionSurvey, created_by=organization).questionnaire_text
        initial = [{'question': q} for q in questions]
        formset = self.AdoptionSurveyFormSet(initial=initial)
        return render(request, 'adopt-form-edit.html', {'formset': formset})

    def post(self, request, *args, **kwargs):
        organization = self.request.user.organization.pk
        formset = self.AdoptionSurveyFormSet(request.POST)
        if formset.is_valid():
            edited_questionnaire_text = {question['question']: '' for question in formset.cleaned_data}
            adopt_form = get_object_or_404(AdoptionSurvey, created_by=organization)
            adopt_form.questionnaire_text = edited_questionnaire_text
            adopt_form.save()
            return redirect(reverse_lazy('dashboard', kwargs={'pk': organization}))
        return render(request, 'adopt-form-edit.html', {'formset': formset})
