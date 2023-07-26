from django.contrib import admin
from django.core.exceptions import ValidationError

from PAWesome.animal.models import Animal, AnimalPhotos
from PAWesome.organization.views import HandleAdoptionForm


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    pass
    # def get_fields(self, request, obj=None):
    #     fields = super().get_fields(request, obj)
    #     if request.user.is_superuser:
    #         fields.append()


@admin.register(AnimalPhotos)
class AnimalPhotosAdmin(admin.ModelAdmin):
    list_display = ('animal', 'is_main_image', 'file_size', 'image_dimensions')

    def save_form(self, request, form, change):
        animal = form.cleaned_data['animal']
        main_image = AnimalPhotos.objects.filter(animal=animal, is_main_image=True).exists()
        if main_image and form.cleaned_data['is_main_image']:
            raise ValidationError('The main image can be only ONE.')
        return super().save_form(request, form, change)


# @admin.register(AdoptedAnimalsArchive)
# class AdoptedAnimalsArchiveAdmin(admin.ModelAdmin):
#     pass
