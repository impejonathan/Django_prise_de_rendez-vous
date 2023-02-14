import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Appointment, Note


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class AppointmentForm(forms.ModelForm):
    nom = forms.CharField(label="Prénom")
    prenom = forms.CharField(label="Nom")
    date = forms.DateField(widget=forms.SelectDateWidget(years=range(2023, 2024)), label="date du rendez-vous")
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="heure du rendez-vous")

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'nom', 'prenom']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        if date and time:
            appointment_start = datetime.datetime.combine(date, time)
            if appointment_start.weekday() > 4:  # 5 est samedi et dimanche
                raise ValidationError("Les rendez-vous peuvent uniquement être pris du lundi au vendredi.")
            if appointment_start.time() < datetime.time(hour=9) or appointment_start.time() > datetime.time(hour=17):
                raise ValidationError("Les rendez-vous peuvent uniquement être pris entre 9h et 17h.")
        end_time = appointment_start + datetime.timedelta(minutes=50)
        appointments = Appointment.objects.filter(date=date, time__range=(appointment_start.time(), end_time.time()))
        if appointments.exists():
            raise ValidationError("Il y a déjà un rendez-vous pris à ce moment.")
        duration = cleaned_data.get("duration")
        if duration and duration.seconds / 60 != 50:
            raise ValidationError("La durée du rendez-vous doit être de 50 minutes.")


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['nom', 'prenom', 'jour_rdv', 'note']
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'jour_rdv': 'Jour du rendez-vous',
            'note': 'Note',
        }
