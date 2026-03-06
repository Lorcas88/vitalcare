from django.contrib import admin
from .models import Paciente, Doctor, Cita

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Doctor)
admin.site.register(Cita)