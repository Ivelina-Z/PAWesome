from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import CharField
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from PAWesome.adoption.forms import AdoptionSurveyForm, FilledAdoptionForm
from PAWesome.adoption.models import SubmittedAdoptionSurvey
from PAWesome.animal.models import Animal, AdoptedAnimalsArchive
from PAWesome.animal.views import BaseAdoptView
from PAWesome.organization.forms import AnimalForm
from PAWesome.organization.mixins import OrganizationMixin
from PAWesome.organization.models import Organization


# PUBLIC PART

def view_all_organizations(request):
    return render(request, 'all-organizations.html')


def view_organization(request, slug):
    return render(request, 'organization-details.html')


# PRIVATE PART


class DashboardView(OrganizationMixin, LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Organization
    template_name = 'dashboard.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.get_organization()
        return queryset.filter(slug=organization.slug)


class AllAnimalsView(OrganizationMixin, LoginRequiredMixin, BaseAdoptView):
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.get_organization()
        return queryset.filter(organization=organization.pk).prefetch_related('photos')


# TODO: Manually written URLs are shown for the other users than the signed
class AddAnimalView(SuccessMessageMixin, OrganizationMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    success_message = 'The animal is added successfully.'
    template_name = 'animal-add.html'
    model = Animal
    form_class = AnimalForm

    def form_valid(self, form):
        form.instance.organization = self.get_organization()
        return super().form_valid(form)

    def get_success_url(self):
        organization = self.get_organization()
        return reverse_lazy('dashboard', kwargs={'slug': organization.slug})


class EditAnimalView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'animal-edit.html'
    model = Animal
    form_class = AnimalForm

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'pk': self.object.pk})


class DeleteAnimalView(OrganizationMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = ['animal.delete_animal', 'animal.delete_animalphotos']
    template_name = 'animal-delete.html'
    model = Animal

    def get_success_url(self):
        organization = self.get_organization()
        return reverse_lazy('organization-animals', kwargs={'slug': organization.slug})


class PendingAdoptForms(OrganizationMixin, LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'waiting-for-approval.html'
    model = SubmittedAdoptionSurvey

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.get_organization()
        return queryset.filter(organization=organization.pk)


class HandleAdoptionForm(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ['animal.add_adoptedanimalsarchive']
    login_url = 'login'
    form_class = FilledAdoptionForm

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return super().dispatch(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)

    def get_form(self, request):
        form = self.form_class(request)
        json_data = SubmittedAdoptionSurvey.objects.get(pk=self.kwargs['pk']).questionnaire_text
        # except:
        for field_name, field_value in json_data.items():
            form.fields[field_name] = CharField(initial=field_value, disabled=True)
        return form

    def get(self, request, *args, **kwargs):
        form = self.get_form(request.GET)
        return render(request, 'waiting-for-approval-details.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form(request.POST)
        if form.is_valid():
            action = request.POST.get('action')
            questionnaire = SubmittedAdoptionSurvey.objects.get(pk=kwargs['pk'])
            if action == 'adopt':
                adopted_animal = AdoptedAnimalsArchive()
                # try:
                animal = Animal.objects.get(pk=questionnaire.animal.pk)
                # except:
                for field in animal._meta.fields:
                    setattr(adopted_animal, field.name, getattr(animal, field.name))
                adopted_animal.filled_questionnaire_text = form.cleaned_data
                adopted_animal.save()

                Animal.delete(animal)
            elif action == 'reject':
                # try:
                questionnaire.delete()
                # except:

            return redirect(reverse_lazy('dashboard', kwargs={'slug': request.user.organization.slug}))
        return render(request, 'waiting-for-approval-details.html', {'form': form})
