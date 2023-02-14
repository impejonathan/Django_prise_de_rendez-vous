from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate , logout
from django.conf import settings

from .forms import AppointmentForm, NoteForm
import datetime
from .models import Appointment, Note
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.template.defaultfilters import wordwrap

from django.utils import timezone
from datetime import timedelta




def index(request):
    return render(request, 
                  'allo_doc/index.html',
                  )
    
def logout_user(request):
    
    logout(request)
    return redirect('login')

# mdp   -----   NEgr7Qu58Uth58  --- <-- le MDP

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                # message = f'Bonjour, {user.username}! Vous êtes connecté.'
                if user.username == 'impe.jonathan.3@gmail.com':
                    return redirect("planning")
                else:
                    return redirect("rdv")
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'allo_doc/login.html', context={'form': form, 'message': message})


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect("login")
    return render(request, 'allo_doc/signup.html', context={'form': form})

@login_required
def rdv(request):
    availability = {}
    now = timezone.now()
    for i in range(3):
        appointment_date = now + timedelta(days=i+1)
        if appointment_date.weekday() < 5:  # skip dimanche  and samedi
            available_times = []
            appointment_start = datetime.combine(appointment_date.date(), datetime.min.time())
            for hour in range(9, 17):
                appointment_time = appointment_start + timedelta(hours=hour)
                end_time = appointment_time + timedelta(minutes=50)
                conflicting_appointments = Appointment.objects.filter(date=appointment_date.date(),
                                                                       time__range=(appointment_time.time(), end_time.time()))
                if not conflicting_appointments:
                    available_times.append(appointment_time.time().strftime('%H:%M'))
            availability[appointment_date.strftime(' le  %d  ')] = available_times

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'allo_doc/rdv_ok.html')
    else:
        form = AppointmentForm()
    return render(request, 'allo_doc/rdv.html', {'form': form, 'availability': availability})



 
@login_required
def rdv_ok(request):
    return render(request, 'allo_doc/rdv_ok.html', )
                  

                 
from datetime import datetime

@login_required
def planning(request):
    if request.user.email != 'impe.jonathan.3@gmail.com':
        return redirect('index')

    now = datetime.now()
    appointments = Appointment.objects.filter(date__gte=now)
    context = {
        'appointments': appointments
    }
    return render(request, 'allo_doc/planning.html', context)

@login_required
def note(request):
    if request.user.email != 'impe.jonathan.3@gmail.com':
        return redirect('index')
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            jour_rdv = form.cleaned_data['jour_rdv']
            note = form.cleaned_data['note']
            note = Note(nom=nom, prenom=prenom, jour_rdv=jour_rdv, note=note)
            note.save()
            return redirect('allo_doc/note_confirm.html')
    else:
        form = NoteForm()
    return render(request, 'allo_doc/note.html', {'form': form})


@login_required
def note_view(request):
    if request.user.email != 'impe.jonathan.3@gmail.com':
        return redirect('index')
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            jour_rdv = form.cleaned_data['jour_rdv']
            note = form.cleaned_data['note']

            note = Note.objects.create(nom=nom, prenom=prenom, jour_rdv=jour_rdv, note=note)
            note.save()
            return redirect('note_confirm')
    else:
        form = NoteForm()
    return render(request, 'allo_doc/note.html', {'form': form})

@login_required
def note_confirm_view(request):
    if request.user.email != 'impe.jonathan.3@gmail.com':
        return redirect('index')
    return render(request, 'allo_doc/note_confirm_view.html')

@login_required
def liste_notes(request):
    if request.user.email != 'impe.jonathan.3@gmail.com':
        return redirect('index')
    notes = Note.objects.all().order_by('nom')

    for note in notes:
        note.note = wordwrap(note.note, 30)

    return render(request, 'allo_doc/liste_notes.html', {'notes': notes})

