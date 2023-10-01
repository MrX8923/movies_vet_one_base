from django.db import models


class Human(models.Model):
    name = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    surname = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    lastname = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.lastname} {self.name} {self.surname}'

    class Meta:
        db_table = 'clinic_human'


class VetDoctor(Human):

    speciality = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'clinic_doctor'


class PetOwner(Human):
    class Meta:
        db_table = 'clinic_pet_owner'


class Pet(models.Model):
    name = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    age = models.IntegerField(
        null=True,
        blank=True
    )
    animal_type = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    specialist = models.ForeignKey(
        VetDoctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    treatment = models.TextField(
        max_length=1000,
        null=True,
        blank=True
    )
    pet_owner = models.ForeignKey(
        PetOwner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    menace = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = 'clinic_pet'
