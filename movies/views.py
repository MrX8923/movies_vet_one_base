from django.shortcuts import render, HttpResponse
from django.views import generic
from .models import *


def index(request):
    data = {
        'movies_count': Movie.objects.all().count(),
        'actors_count': Actor.objects.all().count(),
        'free_count': Movie.objects.filter(subscription__movie=1).count()
    }
    return render(request, 'index.html', context=data)


class ListMovies(generic.ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'

# def info(request, id):
#     movie = Movie.objects.using('movies').get(id=id)
#     return HttpResponse(movie.title)


class DetailMovie(generic.DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
