from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'movies_genre'


class Actor(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birthday = models.DateField(max_length=30)
    country = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        db_table = 'movies_actor'


class Country(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'movies_country'


class Director(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        db_table = 'movies_director'


class AgeRating(models.Model):
    choices = (('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'), ('NC-17', 'NC-17'))
    rating = models.CharField(max_length=30, choices=choices)

    def __str__(self):
        return self.rating

    class Meta:
        db_table = 'movies_age_rating'


class Subscription(models.Model):
    choices = (('бесплатно', 'бесплатно'), ('базовая', 'базовая'), ('СУПЕР', 'СУПЕР'))
    name = models.CharField(max_length=30, choices=choices)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'movies_subscription'


class Movie(models.Model):
    title = models.CharField(max_length=30)
    genre = models.ForeignKey(Genre, on_delete=models.SET_DEFAULT, default=1)
    rating = models.FloatField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=500)
    year = models.IntegerField()
    age_rating = models.ForeignKey(AgeRating, on_delete=models.SET_DEFAULT, default=1)
    actors = models.ManyToManyField(Actor)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movies_table'

    def display_actors(self):
        return ', '.join([actor.name + ' ' + actor.surname for actor in self.actors.all()])
    display_actors.short_description = 'Актеры'

    def get_absolute_url(self):
        return reverse('info', args=[self.id, self.title])


models_tuple = (Genre, Country, AgeRating, Subscription)
