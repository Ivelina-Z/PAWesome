from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.core.exceptions import ValidationError

from PAWesome.animal.forms import AnimalForm
from PAWesome.animal.models import Animal, AnimalPhotos, AdoptedAnimalsArchive, AdoptedAnimalPhotosArchive
from PAWesome.mixins import OnlyViewToIsStaffUsersMixin, OrganizationMixin


@admin.register(Animal)
class AnimalAdmin(OrganizationMixin, gis_admin.GeoModelAdmin):
    default_lat = 42.930
    default_lon = 26.027
    default_zoom = 7
    exclude = ['date_of_publication']
    form = AnimalForm
    change_form_template = 'gis/admin/change_form.html'
    list_filter = (
        'animal_type',
        'gender',
        'sprayed',
        'vaccinated',
        'current_residence'
    )
    search_fields = ('name', )

    def get_exclude(self, request, obj=None):
        exclude_fields = super().get_exclude(request, obj)
        if not request.user.is_superuser:
            exclude_fields.append('organization')
        return exclude_fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if not change:
                obj.organization = self.get_organization()
        return super().save_model(request, obj, form, change)


@admin.register(AnimalPhotos)
class AnimalPhotosAdmin(admin.ModelAdmin):
    list_display = ('animal', 'is_main_image', 'file_size', 'image_dimensions')

    def save_form(self, request, form, change):
        animal = form.cleaned_data['animal']
        main_image = AnimalPhotos.objects.filter(animal=animal, is_main_image=True).exists()
        if main_image and form.cleaned_data['is_main_image']:
            raise ValidationError('The main image can be only ONE.')
        return super().save_form(request, form, change)


@admin.register(AdoptedAnimalsArchive)
class AdoptedAnimalsArchiveAdmin(OnlyViewToIsStaffUsersMixin, admin.ModelAdmin):
    pass


@admin.register(AdoptedAnimalPhotosArchive)
class AdoptedAnimalPhotosArchiveAdmin(OnlyViewToIsStaffUsersMixin, admin.ModelAdmin):
    pass
