from django.db import models
from django.utils import timezone
from django.db.models.functions import ExtractYear, Now
from django.db.models import Func

# Create your models here.
class Paciente(models.Model):
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    # edad = models.IntegerField()
    fecha_nacimiento = models.DateField()

    def calcular_edad(self):
        today = timezone.localdate()  # transform datetime to date
        fn = self.fecha_nacimiento

        # add a year if the month and day are greater or equal
        añadir_año = 0
        if today.month >= fn.month:
            if today.day >= fn.day:
                añadir_año = 1

        return (today.year - fn.year) + añadir_año
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Doctor(models.Model):
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    # edad = models.IntegerField()
    fecha_nacimiento = models.DateField()
    especialidad = models.CharField(max_length=120)

    def calcular_edad(self):
        today = timezone.localdate()  # transform datetime to date
        fn = self.fecha_nacimiento

        # add a year if the month and day are greater or equal
        añadir_año = 0
        if today.month >= fn.month:
            if today.day >= fn.day:
                añadir_año = 1

        return (today.year - fn.year) + añadir_año
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()

    def __str__(self):
        return f"El paciente {self.paciente} tiene cita con el médico: {self.doctor}"