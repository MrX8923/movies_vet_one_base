from django.shortcuts import render, HttpResponse
from django.views import generic
from .models import *
from django.contrib.auth.models import User
from .db_maker import *


def index(request):
    data = {
        'movies_count': Movie.objects.all().count(),
        'actors_count': Actor.objects.all().count(),
        'free_count': Movie.objects.filter(subscription_id=1).count(),
        'username': request.user.first_name if hasattr(request.user, 'first_name') else 'Гость'
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
    paginate_by = 6

# def info(request, id):
#     movie = Movie.objects.using('movies').get(id=id)
#     return HttpResponse(movie.title)


class DetailMovie(generic.DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    extra_context = {'title': 'Фильм'}


class ListActors(generic.ListView):
    model = Actor
    template_name = 'movies/actor_list.html'
    context_object_name = 'actors'
    extra_context = {'title': 'Актеры'}
    paginate_by = 20


class DetailActor(generic.DetailView):
    model = Actor
    template_name = 'movies/actor_detail.html'
    context_object_name = 'actor'
    extra_context = {'title': 'Актер'}


class ListDirectors(generic.ListView):
    model = Director
    template_name = 'movies/director_list.html'
    context_object_name = 'directors'
    extra_context = {'title': 'Режиссеры'}
    paginate_by = 20


class DetailDirector(generic.DetailView):
    model = Director
    template_name = 'movies/director_detail.html'
    context_object_name = 'director'
    extra_context = {'title': 'Режиссер'}


def subscription(request):
    data = {
        'subscriptions': Subscription.objects.all(),
    }
    return render(request, 'subscription.html', context=data)


def see_movie(request, id1, id2, id3):
    arr = ['бесплатно', 'базовая', 'СУПЕР']
    arr2 = ['free', 'based', 'super']
    if id3 == 0:
        sub = 1
    else:
        sub = User.objects.get(id=id3).groups.all()[0].id
    if sub >= id2:
        print('ok')
    else:
        print('neok')
    return render(request, 'index.html')


def make_db(request):
    get_movies()
    return render(request, 'index.html')
