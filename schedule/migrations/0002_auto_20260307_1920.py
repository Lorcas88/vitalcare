# https://docs.djangoproject.com/en/6.0/topics/migrations/#data-migrations
# https://docs.djangoproject.com/en/6.0/howto/writing-migrations/
from django.db import migrations
from datetime import date

def load_initial_data(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Specialty = apps.get_model("schedule", "Specialty")
    Patient = apps.get_model("schedule", "Patient")
    Provider = apps.get_model("schedule", "Provider")

    specialties = [
        "Medicina general",
        "Cardiología",
        "Pediátrica",
        "Cirugía",
        "Dermatología",
        "Obstetricia Ginecología",
        "Otorrinolaringología",
        "Gastroenterología",
    ]

    # https://docs.djangoproject.com/en/6.0/ref/models/querysets/#get-or-create
    specialty_objects = {}
    for name in specialties:
        obj, _ = Specialty.objects.get_or_create(name=name)
        specialty_objects[name] = obj

    Provider.objects.get_or_create(
        first_name = "Martín",
        last_name = "González",
        date_birth = date(2000, 2, 21),
        specialty = specialty_objects["Medicina general"]
    )

    Patient.objects.get_or_create(
        first_name = "Lupita",
        last_name = "Merida",
        date_birth = date(2010, 4, 21)
    )

def reverse_data(apps, schema_editor):
    Specialty = apps.get_model("schedule", "Specialty")
    Patient = apps.get_model("schedule", "Patient")
    Provider = apps.get_model("schedule", "Provider")
    
    # https://docs.djangoproject.com/en/6.0/ref/models/querysets/#delete
    Specialty.objects.all().delete()
    Patient.objects.all().delete()
    Provider.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    # https://docs.djangoproject.com/en/6.0/ref/migration-operations/#runpython
    operations = [
        migrations.RunPython(load_initial_data)
    ]
