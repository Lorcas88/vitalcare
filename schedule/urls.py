from django.urls import path

from . import views


app_name = "schedule"
urlpatterns = [
    # Patients
    path("patient/", views.PatientIndexView.as_view(), name="index_patient"),
    path("patient/create", views.PatientCreateView.as_view(), name="create_patient"),
    path("patient/update/<int:pk>", views.PatientUpdateView.as_view(), name="update_patient"),
    path("patient/delete/<int:pk>", views.PatientDeleteView.as_view(), name="delete_patient"),

    # Providers
    path("provider/", views.ProviderIndexView.as_view(), name="index_provider"),
    path("provider/create", views.ProviderCreateView.as_view(), name="create_provider"),
    path("provider/update/<int:pk>", views.ProviderUpdateView.as_view(), name="update_provider"),
    path("provider/delete/<int:pk>", views.ProviderDeleteView.as_view(), name="delete_provider"),

    # Appointments
    path("", views.IndexView.as_view(), name="index"),
    path("appointment/create", views.AppointmentCreateView.as_view(), name="create_appointment"),
    path("appointment/update/<int:pk>", views.AppointmentUpdateView.as_view(), name="update_appointment"),
    path("appointment/delete/<int:pk>", views.AppointmentDeleteView.as_view(), name="delete_appointment"),
]