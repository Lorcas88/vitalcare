from django.db import models
from django.utils import timezone

from django.core.exceptions import ValidationError

from .config import AGENDA_CONFIG

# Create your models here.
class Specialty(models.Model):
    name = models.CharField("Especialidad", max_length=100, unique=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    first_name = models.CharField("Nombre", max_length=50)
    last_name = models.CharField("Apellido", max_length=50)
    date_birth = models.DateField("Fecha de nacimiento")

    @property
    def age(self):
        today = timezone.localdate()  # transform datetime to date
        bday = self.date_birth

        # add a year if the actual month and day are less or equal
        age_adjustment = today.month <= bday.month and today.day <= bday.day
        return (today.year - bday.year) - age_adjustment
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        

class Patient(Person):
    class Meta:
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"


class Provider(Person):
    specialty = models.ForeignKey(
        Specialty, verbose_name="Especialidad", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "doctor"
        verbose_name_plural = "doctores"


class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient, verbose_name="Paciente", related_name="patient", on_delete=models.PROTECT
    )
    provider = models.ForeignKey(
        Provider, verbose_name="Especialista", related_name="provider", on_delete=models.PROTECT
    )
    datetime_appt = models.DateTimeField("Cita")
    reason = models.ForeignKey(
        Specialty, verbose_name="Motivo", related_name="reason", on_delete=models.PROTECT
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["provider", "datetime_appt"], name="unique_appointment")
        ]
        verbose_name = "cita"
        verbose_name_plural = "citas"
    

    # https://docs.djangoproject.com/en/6.0/ref/models/instances/#django.db.models.Model.clean
    def clean(self):
        dt = self.datetime_appt
        today = timezone.localtime(timezone.now())
        
        if dt.date() < today.date():
            raise ValidationError("La reserva debe ser desde el día actual en adelante.")

        if dt.date() == today.date() and dt.time() < today.time():
            raise ValidationError("La reserva debe ser una hora mayor a la actual.")
        
        if dt.weekday() not in AGENDA_CONFIG["WORKING_DAYS"]:
            raise ValidationError("Las citas deben ser días laborales.")
        
        if not AGENDA_CONFIG["START_TIME"] <= dt.time() < AGENDA_CONFIG["END_TIME"]:
            raise ValidationError("La cita está fuera del horario de atención.")
        
        if dt.minute % AGENDA_CONFIG["SLOT_MINUTES"] != 0:
            raise ValidationError("La cita debe coincidir con un bloque válido.")
        
    def __str__(self):
        return f"{self.datetime_appt} - {self.patient.first_name} {self.patient.last_name} - {self.provider.first_name} {self.provider.last_name} - {self.reason}"