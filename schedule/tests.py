from datetime import date, datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Appointment, Patient, Provider, Specialty


def next_working_date(days_ahead=1):
    current = timezone.localdate() + timedelta(days=days_ahead)
    while current.weekday() > 4:
        current += timedelta(days=1)
    return current


def next_weekend_date(days_ahead=1):
    current = timezone.localdate() + timedelta(days=days_ahead)
    while current.weekday() < 5:
        current += timedelta(days=1)
    return current


def local_aware_datetime(value_date, hour, minute):
    return timezone.make_aware(datetime.combine(value_date, time(hour=hour, minute=minute)))


class BaseScheduleViewTests(TestCase):
    def setUp(self):
        Appointment.objects.all().delete()
        Provider.objects.all().delete()
        Patient.objects.all().delete()
        Specialty.objects.all().delete()

        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="TestPass123!",
        )
        self.client.force_login(self.user)

        self.specialty = Specialty.objects.create(name="Medicina general")
        self.reason = Specialty.objects.create(name="Cardiologia")

        self.patient1 = Patient.objects.create(
            first_name="Carlos",
            last_name="Gonzalez",
            date_of_birth=date(1976, 3, 17),
        )
        self.patient2 = Patient.objects.create(
            first_name="Lupita",
            last_name="Montanosa",
            date_of_birth=date(2010, 6, 10),
        )

        self.provider1 = Provider.objects.create(
            first_name="Martin",
            last_name="Gonzalez",
            date_of_birth=date(1980, 5, 12),
            specialty=self.specialty,
        )
        self.provider2 = Provider.objects.create(
            first_name="Ana",
            last_name="Suarez",
            date_of_birth=date(1988, 8, 22),
            specialty=self.specialty,
        )

        self.appointment1 = Appointment.objects.create(
            patient=self.patient1,
            provider=self.provider1,
            datetime_appt=local_aware_datetime(next_working_date(1), 9, 0),
            reason=self.reason,
        )
        self.appointment2 = Appointment.objects.create(
            patient=self.patient2,
            provider=self.provider2,
            datetime_appt=local_aware_datetime(next_working_date(2), 10, 30),
            reason=self.reason,
        )


class PatientViewTests(BaseScheduleViewTests):
    def setUp(self):
        super().setUp()
        self.index = "schedule:index_patient"
        self.create = "schedule:create_patient"
        self.update = "schedule:update_patient"
        self.delete = "schedule:delete_patient"

    def test_view_patients(self):
        response = self.client.get(reverse(self.index))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["object_list"]), [self.patient1, self.patient2])

    def test_create_patient(self):
        response = self.client.post(
            reverse(self.create),
            {
                "first_name": "Testardo",
                "last_name": "Jimenez",
                "date_of_birth": "1900-03-30",
            },
        )

        self.assertRedirects(response, reverse(self.index))
        self.assertTrue(
            Patient.objects.filter(
                first_name="Testardo",
                last_name="Jimenez",
                date_of_birth=date(1900, 3, 30),
            ).exists()
        )

    def test_update_patient(self):
        response = self.client.post(
            reverse(self.update, args=[self.patient1.pk]),
            {
                "first_name": "Testardo",
                "last_name": "Jimenez",
                "date_of_birth": "1980-03-30",
            },
        )

        self.assertRedirects(response, reverse(self.index))
        self.patient1.refresh_from_db()
        self.assertEqual(self.patient1.first_name, "Testardo")
        self.assertEqual(self.patient1.date_of_birth, date(1980, 3, 30))

    def test_delete_patient(self):
        deletable_patient = Patient.objects.create(
            first_name="Elena",
            last_name="Rojas",
            date_of_birth=date(1995, 7, 20),
        )
        response = self.client.post(reverse(self.delete, args=[deletable_patient.pk]))

        self.assertRedirects(response, reverse(self.index))
        self.assertFalse(Patient.objects.filter(pk=deletable_patient.pk).exists())


class ProviderViewTests(BaseScheduleViewTests):
    def setUp(self):
        super().setUp()
        self.index = "schedule:index_provider"
        self.create = "schedule:create_provider"
        self.update = "schedule:update_provider"
        self.delete = "schedule:delete_provider"

    def test_view_providers(self):
        response = self.client.get(reverse(self.index))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["object_list"]), [self.provider1, self.provider2])

    def test_create_provider(self):
        response = self.client.post(
            reverse(self.create),
            {
                "first_name": "Laura",
                "last_name": "Perez",
                "date_of_birth": "1990-01-15",
                "specialty": self.specialty.pk,
            },
        )

        self.assertRedirects(response, reverse(self.index))
        self.assertTrue(
            Provider.objects.filter(
                first_name="Laura",
                last_name="Perez",
                date_of_birth=date(1990, 1, 15),
                specialty=self.specialty,
            ).exists()
        )

    def test_update_provider(self):
        response = self.client.post(
            reverse(self.update, args=[self.provider1.pk]),
            {
                "first_name": "Pedro",
                "last_name": "Ramirez",
                "date_of_birth": "1985-04-10",
                "specialty": self.specialty.pk,
            },
        )

        self.assertRedirects(response, reverse(self.index))
        self.provider1.refresh_from_db()
        self.assertEqual(self.provider1.first_name, "Pedro")
        self.assertEqual(self.provider1.date_of_birth, date(1985, 4, 10))

    def test_delete_provider(self):
        deletable_provider = Provider.objects.create(
            first_name="Laura",
            last_name="Molina",
            date_of_birth=date(1992, 11, 3),
            specialty=self.specialty,
        )
        response = self.client.post(reverse(self.delete, args=[deletable_provider.pk]))

        self.assertRedirects(response, reverse(self.index))
        self.assertFalse(Provider.objects.filter(pk=deletable_provider.pk).exists())


class AppointmentViewTests(BaseScheduleViewTests):
    def setUp(self):
        super().setUp()
        self.index = "schedule:index"
        self.create = "schedule:create_appointment"
        self.update = "schedule:update_appointment"
        self.delete = "schedule:delete_appointment"

    def test_view_appointments(self):
        response = self.client.get(reverse(self.index))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            [self.appointment1, self.appointment2],
        )

    def test_create_appointment(self):
        appointment_date = next_working_date(3)

        response = self.client.post(
            reverse(self.create),
            {
                "patient": self.patient1.pk,
                "provider": self.provider2.pk,
                "appt_date": appointment_date.isoformat(),
                "appt_time": "11:00",
                "reason": self.reason.pk,
            },
        )

        self.assertRedirects(response, reverse(self.index))
        self.assertTrue(
            Appointment.objects.filter(
                patient=self.patient1,
                provider=self.provider2,
                datetime_appt__date=appointment_date,
                datetime_appt__hour=11,
                datetime_appt__minute=0,
                reason=self.reason,
            ).exists()
        )

    def test_update_appointment(self):
        appointment_date = next_working_date(4)

        response = self.client.post(
            reverse(self.update, args=[self.appointment1.pk]),
            {
                "patient": self.patient2.pk,
                "provider": self.provider1.pk,
                "appt_date": appointment_date.isoformat(),
                "appt_time": "12:30",
                "reason": self.reason.pk,
            },
        )

        self.assertRedirects(response, reverse(self.index))
        self.appointment1.refresh_from_db()
        local_dt = timezone.localtime(self.appointment1.datetime_appt)
        self.assertEqual(self.appointment1.patient, self.patient2)
        self.assertEqual(local_dt.date(), appointment_date)
        self.assertEqual(local_dt.time().hour, 12)
        self.assertEqual(local_dt.time().minute, 30)

    def test_delete_appointment(self):
        response = self.client.post(reverse(self.delete, args=[self.appointment2.pk]))

        self.assertRedirects(response, reverse(self.index))
        self.assertFalse(Appointment.objects.filter(pk=self.appointment2.pk).exists())

    def test_create_appointment_rejects_weekend_booking(self):
        appointment_date = next_weekend_date(1)

        response = self.client.post(
            reverse(self.create),
            {
                "patient": self.patient1.pk,
                "provider": self.provider1.pk,
                "appt_date": appointment_date.isoformat(),
                "appt_time": "09:00",
                "reason": self.reason.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Las citas deben ser días laborales.",
        )
        self.assertFalse(
            Appointment.objects.filter(
                patient=self.patient1,
                provider=self.provider1,
                datetime_appt__date=appointment_date,
                datetime_appt__hour=9,
                datetime_appt__minute=0,
            ).exists()
        )
