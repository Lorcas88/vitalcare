from django.contrib import admin

from .models import Specialty, Provider, Patient, Appointment

admin.site.register([Specialty, Provider, Patient, Appointment])