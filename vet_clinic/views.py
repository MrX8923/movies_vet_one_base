from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


def index(request):
    data = {
        'animals_count': Pet.objects.all().count(),
        'owners_count': PetOwner.objects.all().count(),
        'specs_count': VetDoctor.objects.all().count(),
        'tittle': 'Главная'
    }
    return render(request, 'index.html', context=data)


class ListPets(ListView):
    template_name = 'vet_clinic/pets_list.html'
    model = Pet
    context_object_name = 'pets'


class DetailPet(DetailView):
    template_name = 'vet_clinic/pet_detail.html'
    model = Pet
    context_object_name = 'pet'
