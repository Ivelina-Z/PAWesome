from django.contrib import admin

from PAWesome.animal.models import Animal, AnimalPhotos


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    pass


@admin.register(AnimalPhotos)
class AnimalPhotosAdmin(admin.ModelAdmin):
    pass
