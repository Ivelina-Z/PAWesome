from django.contrib import admin

from PAWesome.animal.models import Animal, AnimalPhotos, AdoptedAnimalsArchive


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    pass


@admin.register(AnimalPhotos)
class AnimalPhotosAdmin(admin.ModelAdmin):
    list_display = ('animal', 'is_main_image', 'file_size', 'image_dimensions')


@admin.register(AdoptedAnimalsArchive)
class AdoptedAnimalsArchiveAdmin(admin.ModelAdmin):
    pass
