from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import inlineformset_factory
from django.forms.utils import ErrorList
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from PAWesome.animal.forms import AnimalForm, AnimalPhotoForm, FilterAnimalForm
from PAWesome.animal.models import Animal, AnimalPhotos
from PAWesome.animal.validators import validate_one_main_image
from PAWesome.mixins import OrganizationMixin


class BaseAdoptView(ListView):
    model = Animal
    template_name = 'adopt.html'
    ordering = 'date_of_publication'
    # paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'organization' in self.request.GET:
            queryset = queryset.filter(organization=self.request.GET['organization'])

        form = FilterAnimalForm(self.request.GET)
        if form.is_valid():
            fields_allowed_none = ['sprayed', 'vaccinated']
            filters = {}
            for field_name, field_value in form.cleaned_data.items():
                if field_value != 'all':
                    if field_name in fields_allowed_none and (field_value is None or field_value == ''):
                        filters[field_name] = None
                    elif field_value is not None and field_value != '':
                        filters[field_name] = field_value

            if filters:
                queryset = queryset.filter(
                    **filters
                )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilterAnimalForm(self.request.GET)
        return context


class AnimalDetailsView(OrganizationMixin, DetailView):
    model = Animal
    template_name = 'animal_detail.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('animalphotos_set')


class AddAnimalView(SuccessMessageMixin, OrganizationMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    success_message = 'Това животно е успешно добавено.'
    template_name = 'animal-add.html'
    model = Animal
    form_class = AnimalForm
    AnimalPhotoFormSet = inlineformset_factory(Animal, AnimalPhotos, form=AnimalPhotoForm, extra=1)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.method == 'POST':
            form.formset = self.AnimalPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            form.formset = self.AnimalPhotoFormSet(instance=self.object)
        return form

    def form_valid(self, form):
        form.instance.organization = self.get_organization()
        formset = form.formset
        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.is_main_image = True
                instance.animal = form.instance
                instance.save()
            return super().form_valid(form)
        formset_errors = formset.errors
        form_errors = form._errors.setdefault('__all__', ErrorList())
        form_errors.extend(formset_errors)
        return super().form_invalid(form)

    def get_success_url(self):
        organization = self.get_organization()
        return reverse_lazy('dashboard', kwargs={'slug': organization.slug})


class EditAnimalView(LoginRequiredMixin, OrganizationMixin, UpdateView):
    login_url = 'login'
    template_name = 'animal-edit.html'
    model = Animal
    form_class = AnimalForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                animal = self.model.objects.get(pk=kwargs['pk'])
                if self.get_organization() != animal.organization:
                    raise Http404('Това животно не съществува.')
            except self.model.DoesNotExist:
                raise Http404('Това животно не съществува.')
        return super().dispatch(request, *args, **kwargs)

    def get_animal_photo_formset(self):
        has_photo = self.object.animalphotos_set.exists()
        extra = 0 if has_photo else 1
        animal_photo_formset = inlineformset_factory(
            Animal,
            AnimalPhotos,
            form=AnimalPhotoForm,
            extra=extra
        )
        return animal_photo_formset

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        AnimalPhotoFormSet = self.get_animal_photo_formset()
        if self.request.method == 'POST':
            form.formset = AnimalPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            form.formset = AnimalPhotoFormSet(instance=self.object)
        return form

    def form_valid(self, form):
        # photos = AnimalPhotos.objects.get(animal=self.object.pk)
        formset = form.formset
        if form.is_valid() and formset.is_valid():
            try:
                validate_one_main_image(formset)
            except KeyError:
                pass
            # total_main_images = 0
            # for instance in formset:
            #     if instance.cleaned_data['is_main_image']:
            #         total_main_images += 1
            #     if total_main_images > 1:
            #         raise ValidationError('The main image can be only ONE.')
            form.save()
            formset.save()
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('animal-details', kwargs={'pk': self.object.pk})


class DeleteAnimalView(OrganizationMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = ['animal.delete_animal', 'animal.delete_animalphotos']
    template_name = 'animal-delete.html'
    model = Animal

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                animal = self.model.objects.get(pk=kwargs['pk'])
                if self.get_organization() != animal.organization:
                    raise Http404('Това животно не съществува.')
            except self.model.DoesNotExist:
                raise Http404('Това животно не съществува.')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        organization = self.get_organization()
        return reverse_lazy('organization-animals', kwargs={'slug': organization.slug})
