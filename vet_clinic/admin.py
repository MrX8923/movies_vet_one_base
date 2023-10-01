from django.contrib import admin
from .models import *


# class HumanTable(admin.ModelAdmin):
#     list_display = ('name', 'surname', 'lastname')
#     list_display_links = ('name', 'surname', 'lastname')
#
#
# admin.site.register(Human, HumanTable)


class VetDoctorTable(admin.ModelAdmin):
    list_display = ('name', 'surname', 'lastname', 'speciality')
    list_display_links = ('name', 'surname', 'lastname', 'speciality')


admin.site.register(VetDoctor, VetDoctorTable)


class PetOwnerTable(admin.ModelAdmin):
    list_display = ('name', 'surname', 'lastname')
    list_display_links = ('name', 'surname', 'lastname')


admin.site.register(PetOwner, PetOwnerTable)


class PetTable(admin.ModelAdmin):
    list_display = ('name', 'age', 'animal_type', 'specialist', 'pet_owner')
    list_filter = ('specialist', 'pet_owner', 'menace')
    fieldsets = (
        ('О звере', {'fields': ('name', 'animal_type', 'age', 'menace', 'pet_owner')}),
        ('Лечение', {'fields': ('specialist', 'treatment')})
    )


admin.site.register(Pet, PetTable)
