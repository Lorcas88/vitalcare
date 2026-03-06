from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.views import generic

from .models import Paciente, Doctor, Cita

# Create your views here.
class PacienteIndexView(generic.ListView):
    model = Paciente
    extra_context = {
        "title": "Pacientes",
        "detail_url_name": "agenda:paciente-detail"
    }
    template_name = "agenda/list.html"


class PacienteDetailView(generic.DetailView):
    model = Paciente
    template_name = "agenda/detail.html"


class DoctorIndexView(generic.ListView):
    model = Doctor
    extra_context = {
        "title": "Doctores",
        "detail_url_name": "agenda:doctor-detail"
    }
    template_name = "agenda/list.html"


class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = "agenda/detail.html"


class CitaIndexView(generic.ListView):
    model = Cita
    # https://docs.djangoproject.com/en/6.0/ref/class-based-views/mixins-simple/#contextmixin
    extra_context = {
        "title": "Citas",
        # dict value to make one template per view.
        # it passes the detail view, 'cause the table on list
        # shows with the url to view the detail of the value
        "detail_url_name": "agenda:cita-detail"
    }
    template_name = "agenda/list.html"

class CitaDetailView(generic.DetailView):
    model = Cita
    template_name = "agenda/detail.html"
