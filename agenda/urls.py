from django.urls import path

from . import views

app_name = "agenda"
urlpatterns = [
    path("pacientes/", views.PacienteIndexView.as_view(), name="paciente-list"),
    path("pacientes/<int:pk>/", views.PacienteDetailView.as_view(), name="paciente-detail"),
    path("doctores/", views.DoctorIndexView.as_view(), name="doctor-list"),
    path("doctores/<int:pk>/", views.DoctorDetailView.as_view(), name="doctor-detail"),
    path("citas/", views.CitaIndexView.as_view(), name="citas-list"),
    path("citas/<int:pk>/", views.CitaDetailView.as_view(), name="citas-detail"),
]