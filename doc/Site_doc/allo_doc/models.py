from django.db import models
import datetime
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField(default=datetime.timedelta(minutes=50))

def clean(self):
    if not self.nom:
        raise ValidationError("Le nom n'est pas défini.")
    if not self.prenom:
        raise ValidationError("Le prénom n'est pas défini.")
    if not self.time:
        raise ValidationError("Le temps n'est pas défini.")
    if not self.date:
        raise ValidationError("La date n'est pas définie.")
    if not self.duration:
        self.duration = datetime.timedelta(hours=1)
    appointment_start = datetime.datetime.combine(self.date, self.time)
    appointment_end = appointment_start + self.duration
    appointments = Appointment.objects.filter(
        date=self.date,
        time__gt=(appointment_start - datetime.timedelta(minutes=10)),
        time__lt=(appointment_end + datetime.timedelta(minutes=10)),
    ).exclude(id=self.id)
    if appointments:
        raise ValidationError("Il y a déjà un rendez-vous à cette heure.")
    


class Note(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    jour_rdv = models.DateField()
    note = models.TextField()

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.jour_rdv})"

