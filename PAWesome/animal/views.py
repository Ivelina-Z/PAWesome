from django.views.generic import ListView, DetailView, FormView

from PAWesome.animal.models import Animal


class BaseAdoptView(ListView):
    model = Animal  # TODO: Use the Animal Photo model as well
    template_name = 'adopt.html'
    ordering = '-date_of_publication'
    paginate_by = 3  # TODO: Change to more


class AdoptCatView(BaseAdoptView):
    def get_queryset(self):
        return super().get_queryset().filter(animal_type='cat').prefetch_related('photos')


class AdoptDogView(BaseAdoptView):
    def get_queryset(self):
        return super().get_queryset().filter(animal_type='dog').prefetch_related('photos')


class AdoptBunnyView(BaseAdoptView):
    def get_queryset(self):
        return super().get_queryset().filter(animal_type='bunny').prefetch_related('photos')


class AnimalDetailsView(DetailView):
    model = Animal
    template_name = 'animal_detail.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('photos')
