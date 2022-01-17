from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone


class Doctor(models.Model):
    name = models.CharField(max_length=42)
    email = models.CharField(max_length=42)
    password = models.CharField(max_length=42)

    def __str__(self):
        """
        This method that we will define in all models
        will allow us to easily recognize the different objects that
        we will deal later in the administration
        """
        return self.name


class Patient(models.Model):
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    age = models.IntegerField()
    TZ = models.CharField(max_length=20)
    birthDate = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        ordering = ['age']

    def __str__(self):
        """
        This method that we will define in all models
        will allow us to easily recognize the different objects that
        we will deal later in the administration
        """
        return self.first_name + " " + self.last_name


class File(models.Model):
    title = models.CharField(max_length=100)
    record_date = models.DateField(default=timezone.now)
    file_date = models.DateField(default=timezone.now)
    start_time = models.DateTimeField(default=timezone.now)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    class Meta:
        ordering = ['record_date']

    def __str__(self):
        """
        This method that we will define in all models
        will allow us to easily recognize the different objects that
        we will deal later in the administration
        """
        return self.title + " of " + self.patient.__str__()


def _(param):
    pass


class RecordingFile(models.Model):
    title = models.CharField(max_length=20)
    ecgfile = models.FileField(upload_to='ECG/patient')
    url = models.CharField(max_length=200)
    doctor = models.CharField(max_length=20)
    patient = models.CharField(max_length=20)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        This method that we will define in all models
        will allow us to easily recognize the different objects that
        we will deal later in the administration
        """
        return self.title

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            self.delete(name)
        return name
