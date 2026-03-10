from datetime import datetime, time

from django import forms
from django.utils import timezone

from .service import generate_time_choices
from .models import Patient, Provider, Appointment


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"
        widgets = {
            "date_birth": forms.DateInput(attrs={"type": "date"})
        }


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = "__all__"
        widgets = {
            "date_birth": forms.DateInput(attrs={"type": "date"})
        }


class AppointmentForm(forms.ModelForm):
    appt_date = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    appt_time = forms.ChoiceField(
        label="Hora",
        choices=[],
    )

    class Meta:
        model = Appointment
        fields = ["patient", "provider", "appt_date", "appt_time", "reason"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["appt_time"].choices = generate_time_choices()

        # If it's updating an existing appointment
        if self.instance.pk and self.instance.datetime_appt:
            local_dt = timezone.localtime(self.instance.datetime_appt)
            self.fields["appt_date"].initial = local_dt.date()
            self.fields["appt_time"].initial = local_dt.strftime("%H:%M")

    def clean(self):
        # Retrieve the info as an object
        cleaned_data = super().clean()
        appt_date = cleaned_data.get("appt_date")
        appt_time = cleaned_data.get("appt_time")

        # Combine date and time with the date
        if appt_date and appt_time:
            hour = int(appt_time.split(":")[0]) 
            minute = int(appt_time.split(":")[1])
            dt = datetime.combine(
                appt_date, time(hour=hour, minute=minute)
            )
            cleaned_data["datetime_appt"] = dt
            self.instance.datetime_appt = dt
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.datetime_appt = self.cleaned_data["datetime_appt"]

        if commit:
            instance.save()
        return instance