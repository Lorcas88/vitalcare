from datetime import date, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import AppointmentForm, PatientForm, ProviderForm
from .models import Appointment, Patient, Provider

def format_cell_value(value):
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y %H:%M")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return value

def build_table_config(model, object_list):
    entity = model._meta.verbose_name
    entity_plural = model._meta.verbose_name_plural

    columns = [
        {"name": f.name, "label": f.verbose_name}
        for f in model._meta.fields
        if not f.auto_created
    ]

    rows = [
        {
            "pk": obj.pk,
            "cells": [
                format_cell_value(getattr(obj, col["name"]))
                for col in columns
            ],
        }
        for obj in object_list
    ]

    model_name = model._meta.model_name
        
    return {
        "title": f"Listado de {entity_plural}",
        "title_create": f"Crear {entity}",
        "create_url_name": f"schedule:create_{model_name}",
        "edit_url_name": f"schedule:update_{model_name}",
        "delete_url_name": f"schedule:delete_{model_name}",
        "no_values": f"No hay {entity_plural} inscritos.",
        "rows": rows,
        "columns": [
            {"name": f.name, "label": f.verbose_name}
            for f in model._meta.fields
            if not f.auto_created
        ],
        "colspan": len(columns) + 2,
    }

# =============== BASE =============== #
class BaseCrudView(LoginRequiredMixin):
    template_name = "schedule/crud.html"

class BaseCreateUpdateView(SuccessMessageMixin, BaseCrudView):
    pass

class BaseDeleteView(SuccessMessageMixin, BaseCrudView, DeleteView):
    pass

class BaseEntityListView(LoginRequiredMixin, ListView):
    template_name = "schedule/index.html"

    # https://docs.djangoproject.com/en/6.0/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin.get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_config"] = build_table_config(self.model, context["object_list"])
        return context


# =============== Patient =============== #
class PatientIndexView(BaseEntityListView):
    model = Patient
    
class PatientCreateView(BaseCreateUpdateView, CreateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy("schedule:index_patient")
    extra_context = { "title": "Crear paciente" }
    success_message = "Perfil de paciente registrado exitosamente."

class PatientUpdateView(BaseCreateUpdateView, UpdateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy("schedule:index_patient")
    extra_context = { "title": "Modificar paciente" }
    success_message = "Perfil de paciente editado exitosamente."

class PatientDeleteView(BaseCrudView, DeleteView):
    model = Patient
    success_message = "Perfil de paciente eliminado exitosamente."
    success_url = reverse_lazy("schedule:index_patient")


# =============== Provider =============== #
class ProviderIndexView(BaseEntityListView):
    model = Provider

class ProviderCreateView(BaseCreateUpdateView, CreateView):
    model = Provider
    form_class = ProviderForm
    success_url = reverse_lazy("schedule:index_provider")
    extra_context = { "title": "Crear doctor" }
    success_message = "Perfil de especialista registrado exitosamente."

class ProviderUpdateView(BaseCreateUpdateView, UpdateView):
    model = Provider
    form_class = ProviderForm
    success_url = reverse_lazy("schedule:index_provider")
    extra_context = { "title": "Modificar doctor" }
    success_message = "Perfil de especialista editado exitosamente."

class ProviderDeleteView(BaseCreateUpdateView, DeleteView):
    model = Provider
    success_message = "Perfil de especialista eliminado exitosamente."
    success_url = reverse_lazy("schedule:index_provider")
    

# =============== Appointment =============== #
class IndexView(BaseEntityListView):
    model = Appointment

class AppointmentCreateView(BaseCreateUpdateView, CreateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy("schedule:index")
    extra_context = { "title": "Agendar cita" }
    success_message = "Hora agendada exitosamente."

class AppointmentUpdateView(BaseCreateUpdateView, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy("schedule:index")    
    extra_context = { "title": "Modificar cita" }
    success_message = "Hora reagendada exitosamente."

class AppointmentDeleteView(BaseCreateUpdateView, DeleteView):
    model = Appointment
    success_message = "Cita cancelada exitosamente."
    success_url = reverse_lazy("schedule:index")
    template_name = "schedule/crud.html"
