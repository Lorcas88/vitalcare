from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.views import generic
from django.views.generic.list import ListView

from .models import Appointment, Patient, Provider


# Create your views here.
class IndexView(ListView):
    model = Appointment
    template_name = "schedule/index.html"


# class PatientIndexView(generic.ListView):
#     model = Patient
#     extra_context = {
#         "title": "Pacientes",
#         "detail_url_name": "schedule:patient-detail"
#     }
#     template_name = "schedule/list.html"


class PatientDetailView(generic.DetailView):
    model = Patient
    template_name = "schedule/detail.html"


# class ProviderIndexView(generic.ListView):
#     model = Provider
#     extra_context = {
#         "title": "Doctores",
#         "detail_url_name": "schedule:provider-detail"
#     }
#     template_name = "schedule/list.html"


# class ProviderDetailView(generic.DetailView):
#     model = Provider
#     template_name = "schedule/detail.html"


# class AppointmentIndexView(generic.ListView):
#     model = Appointment
#     # https://docs.djangoproject.com/en/6.0/ref/class-based-views/mixins-simple/#contextmixin
#     extra_context = {
#         "title": "Citas",
#         # dict value to make one template per view.
#         # it passes the detail view, 'cause the table on list
#         # shows with the url to view the detail of the value
#         "detail_url_name": "appointment:cita-detail"
#     }
#     template_name = "schedule/list.html"

# class AppointmentDetailView(generic.DetailView):
#     model = Appointment
#     template_name = "schedule/detail.html"
