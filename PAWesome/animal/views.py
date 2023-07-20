from django.views.generic import ListView, DetailView

from PAWesome.animal.models import Animal


class BaseAdoptView(ListView):
    model = Animal
    template_name = 'adopt.html'
    ordering = 'date_of_publication'
    paginate_by = 10


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
