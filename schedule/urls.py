from django.urls import path

from . import views

app_name = "schedule"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # path("patient/", views.PatientIndexView.as_view(), name="patient-list"),
    path("patient/<int:pk>/", views.PatientDetailView.as_view(), name="patient-detail"),
    # path("doctores/", views.ProviderIndexView.as_view(), name="doctor-list"),
    # path("doctores/<int:pk>/", views.ProviderDetailView.as_view(), name="doctor-detail"),
    # path("citas/", views.AppointmentIndexView.as_view(), name="citas-list"),
    # path("citas/<int:pk>/", views.AppointmentDetailView.as_view(), name="citas-detail"),
]