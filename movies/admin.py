from django.contrib import admin
from .models import *


class ActorTable(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'birthday', 'country')
    list_display_links = ('firstname', 'lastname', 'birthday')


admin.site.register(Actor, ActorTable)


class DirectorTable(admin.ModelAdmin):
    list_display = ('firstname', 'lastname')
    list_display_links = ('firstname', 'lastname')


admin.site.register(Director, DirectorTable)


class MovieTable(admin.ModelAdmin):
    list_display = ('title', 'year', 'director', 'display_actors')
    list_filter = ('subscription', 'genre', 'rating')
    fieldsets = (
        ('О фильме', {'fields': ('title', 'summary', 'actors')}),
        ('Рейтинг', {'fields': ('rating', 'age_rating', 'subscription')}),
        ('Остальное', {'fields': ('director', 'genre', 'year', 'country', 'poster')})
    )


admin.site.register(Movie, MovieTable)

for mod in models_tuple:
    admin.site.register(mod, admin.ModelAdmin)
