from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from PAWesome.animal.forms import AnimalForm, AnimalPhotoForm, FilterAnimalForm
from PAWesome.animal.models import Animal, AnimalPhotos
from PAWesome.mixins import OrganizationMixin


class BaseAdoptView(ListView):
    model = Animal
    template_name = 'adopt.html'
    ordering = 'date_of_publication'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        form = FilterAnimalForm(self.request.GET)
        if form.is_valid():

            filters = {}
            for field_name, field_value in form.cleaned_data.items():
                if field_name != 'medical_issues' and field_value is not None and field_value != '':
                    filters[field_name] = field_value

            if filters:
                queryset = queryset.filter(
                    medical_issues__isnull=not form.cleaned_data['medical_issues'],
                    **filters
                )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilterAnimalForm(self.request.GET)
        return context


class AdoptCatView(BaseAdoptView):
    def get_queryset(self):
        return super().get_queryset().filter(animal_type='cat').prefetch_related('animalphotos_set')


class AdoptDogView(BaseAdoptView):
    def get_queryset(self):
        return super().get_queryset().filter(animal_type='dog').prefetch_related('animalphotos_set')


class AdoptBunnyView(BaseAdoptView):
    def get_queryset(self):
        return super().get_queryset().filter(animal_type='bunny').prefetch_related('animalphotos_set')


class AnimalDetailsView(DetailView):
    model = Animal
    template_name = 'animal_detail.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('animalphotos_set')


# TODO: Manually written URLs are shown for the other users than the signed
class AddAnimalView(SuccessMessageMixin, OrganizationMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    success_message = 'The animal is added successfully.'
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
        if form.formset.is_valid() and form.is_valid():
            form.save()
            formset = form.formset
            instances = formset.save(commit=False)
            for instance in instances:
                instance.is_main_image = True
                instance.animal = form.instance
                instance.save()
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_success_url(self):
        organization = self.get_organization()
        return reverse_lazy('dashboard', kwargs={'slug': organization.slug})


class EditAnimalView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'animal-edit.html'
    model = Animal
    form_class = AnimalForm

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
        if self.request.method == 'POST':
            AnimalPhotoFormSet = self.get_animal_photo_formset()
            form.formset = AnimalPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            AnimalPhotoFormSet = self.get_animal_photo_formset()
            form.formset = AnimalPhotoFormSet(instance=self.object)
        return form

    def form_valid(self, form):
        # photos = AnimalPhotos.objects.get(animal=self.object.pk)
        formset = form.formset
        if form.is_valid() and formset.is_valid():
            total_main_images = 0
            for instance in formset:
                if instance.cleaned_data['is_main_image']:
                    total_main_images += 1
                if total_main_images > 1:
                    raise ValidationError('The main image can be only ONE.')
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

    def get_success_url(self):
        organization = self.get_organization()
        return reverse_lazy('organization-animals', kwargs={'slug': organization.slug})
