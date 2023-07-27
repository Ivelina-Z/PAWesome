from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, UpdateView

from PAWesome.adoption.forms import AdoptionSurveyForm
from PAWesome.adoption.models import AdoptionSurvey, SubmittedAdoptionSurvey
from django.forms import formset_factory, CharField

from PAWesome.animal.models import Animal
from PAWesome.mixins import OrganizationMixin, FormControlMixin
from PAWesome.organization.models import Organization


class AddAdoptionForm(OrganizationMixin, PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ['adoption.add_adoptionsurvey']
    login_url = 'organization-login'
    template_name = 'adopt-form-add.html'
    AdoptionSurveyFormSet = formset_factory(AdoptionSurveyForm, extra=0)

    def get(self, request, *args, **kwargs):
        formset = self.AdoptionSurveyFormSet(initial=[
            {'question': 'Име, Презиме, Фамилия'},
            {'question': 'Телефон за контакт'},
            {'question': 'Имейл'}
        ])
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.AdoptionSurveyFormSet(request.POST)

        if formset.is_valid():
            data = {request.POST.get(f'form-{idx}-question'): '' for idx in range(formset.total_form_count())}
            AdoptionSurvey.objects.create(questionnaire_text=data, created_by_id=request.user.organization.pk)
            organization = self.get_organization()
            return redirect(reverse_lazy('dashboard', kwargs={'slug': organization.slug}))
        return redirect('adopt-form-add')


class EditAdoptForm(OrganizationMixin, PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ['adoption.change_adoptionsurvey']
    login_url = 'organization-login'
    template_name = 'adopt-form-edit.html'
    AdoptionSurveyFormSet = formset_factory(AdoptionSurveyForm, extra=0)

    def get(self, request, *args, **kwargs):
        # try:
        organization = Organization.objects.get(pk=self.get_organization().pk)
        questions = AdoptionSurvey.objects.get(created_by=organization).questionnaire_text
        # except: # TODO: Check what is the error and add it
        #     questions = []
        initial = [{'question': q} for q in questions]
        formset = self.AdoptionSurveyFormSet(initial=initial)
        return render(request, 'adopt-form-edit.html', {'formset': formset})

    def post(self, request, *args, **kwargs):
        organization = self.get_organization()
        formset = self.AdoptionSurveyFormSet(request.POST)
        if formset.is_valid():
            edited_questionnaire_text = {question['question']: '' for question in formset.cleaned_data}
            # try:
            adopt_form = AdoptionSurvey.objects.get(created_by=organization.pk)
            # except:
            #     pass
            adopt_form.questionnaire_text = edited_questionnaire_text
            adopt_form.save()
            return redirect(reverse_lazy('dashboard', kwargs={'slug': organization.slug}))
        return render(request, 'adopt-form-edit.html', {'formset': formset})


class SubmitAdoptForm(SuccessMessageMixin, CreateView):
    success_message = 'Формата за осиновяване е успешно подадена. Ще получите имейл при промяна на нейния статус.'
    template_name = 'submit-adopt-form.html'
    model = SubmittedAdoptionSurvey
    fields = ['email']
    success_url = reverse_lazy('homepage')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # try:
        animal = Animal.objects.get(pk=self.kwargs['pk'])
        # except:
        json_data = AdoptionSurvey.objects.get(created_by=animal.organization).questionnaire_text

        for field_name, field_value in json_data.items():
            form.fields[field_name] = CharField(label=field_name, required=True, initial=field_value)
        return form

    def form_valid(self, form):
        initial_status = 'pending'
        json_form = form.cleaned_data
        animal = get_object_or_404(Animal, pk=self.kwargs['pk'])
        organization = get_object_or_404(Organization, pk=animal.organization.pk)
        form.instance.questionnaire_text = json_form
        form.instance.status = initial_status
        form.instance.animal = animal
        form.instance.organization = organization
        return super().form_valid(form)

