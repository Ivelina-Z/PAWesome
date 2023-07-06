from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from PAWesome.animal.views import BaseAdoptView, AdoptCatView, AdoptDogView, AdoptBunnyView, AnimalDetailsView

urlpatterns = [
    path('animals/', BaseAdoptView.as_view(), name='animals-all'),
    path('adopt/', include([
        path('cat/', AdoptCatView.as_view(), name='adopt-cat'),
        path('dog/', AdoptDogView.as_view(), name='adopt-dog'),
        path('bunny/', AdoptBunnyView.as_view(), name='adopt-bunny')
    ])),
    path('details/<int:pk>', AnimalDetailsView.as_view(), name='animal-details')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
