from django.db import models
from django.utils import timezone
import datetime
from django.contrib.postgres.fields import ArrayField,HStoreField
# Create your models here.


class Doctor(models.Model):
    name = models.CharField(max_length=42)
    email = models.CharField(max_length=42)
    password = models.CharField(max_length=42)

    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard dans l'administration
        """
        return self.name


class Patient(models.Model):
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    age = models.IntegerField()
    TZ = models.CharField(max_length=20)
    birthDate = models.DateField()
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)

    class Meta:
        ordering = ['age']

    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard dans l'administration
        """
        return self.first_name + " " + self.last_name


class File(models.Model):
    title = models.CharField(max_length=100)
    record_date = models.DateField(default = timezone.now)
    file_date = models.DateField(default = timezone.now)
    start_time = models.DateTimeField(default = timezone.now)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)

    class Meta :
        ordering = ['record_date']

    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard dans l'administration
        """
        return self.title + " of " + self.patient.__str__()


def _(param):
    pass


class RecordingFile(models.Model):
    title = models.CharField(max_length=20)
    ecgfile = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    doctor = models.CharField(max_length=20)
    patient = models.CharField(max_length=20)
    datetime = models.DateTimeField(auto_now=True)











    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard dans l'administration
        """
        return self.title