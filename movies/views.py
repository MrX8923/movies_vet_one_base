from django.shortcuts import render, HttpResponse
from django.views import generic
from .models import *
from django.contrib.auth.models import User


def index(request):
    data = {
        'movies_count': Movie.objects.all().count(),
        'actors_count': Actor.objects.all().count(),
        'free_count': Movie.objects.filter(subscription__movie=1).count(),
        'username': request.user.first_name if hasattr(request.user, 'first_name') else 'Guest'
    }
    # user = User.objects.create_user('User3', 'user3@mail.ru', 'useruser')
    # user.first_name = 'Vlad'
    # user.last_name = 'Petrov'
    # user.save()
    return render(request, 'index.html', context=data)


class ListMovies(generic.ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    extra_context = {'title': 'Фильмы'}
    paginate_by = 1

# def info(request, id):
#     movie = Movie.objects.using('movies').get(id=id)
#     return HttpResponse(movie.title)


class DetailMovie(generic.DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    extra_context = {'title': 'Фильм'}
