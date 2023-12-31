from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from PAWesome.animal.views import BaseAdoptView, AnimalDetailsView, AddAnimalView, EditAnimalView, DeleteAnimalView

urlpatterns = [
    path('adopt/', BaseAdoptView.as_view(), name='animals-all'),
    # path('adopt/', include([
    #     path('cat/', AdoptCatView.as_view(), name='adopt-cat'),
    #     path('dog/', AdoptDogView.as_view(), name='adopt-dog'),
    #     path('bunny/', AdoptBunnyView.as_view(), name='adopt-bunny')
    # ])),
    path('animal/', include([
        path('add/', AddAnimalView.as_view(), name='animal-add'),
        path('edit/<int:pk>', EditAnimalView.as_view(), name='animal-edit'),
        path('delete/<int:pk>', DeleteAnimalView.as_view(), name='animal-delete'),
        path('details/<int:pk>', AnimalDetailsView.as_view(), name='animal-details')
    ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
