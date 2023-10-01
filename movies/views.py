from django.shortcuts import render, HttpResponse
from django.views import generic
from .models import *


def index(request):
    data = {
        'movies_count': Movie.objects.all().count(),
        'actors_count': Actor.objects.all().count(),
        'free_count': Movie.objects.filter(subscription__movie=1).count()
    }
    return render(request, '../../dajango_movies_vetclinic_one_base/templates/index.html', context=data)


class MoviesList(generic.ListView):
    model = Movie

# def info(request, id):
#     movie = Movie.objects.using('movies').get(id=id)
#     return HttpResponse(movie.title)


class MovieDetail(generic.DetailView):
    model = Movie
