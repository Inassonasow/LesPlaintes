from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse
from .forms import SignalementForm,CitoyenCreationForm,LoginForm
from .models import Signalement, Citoyen
from django.views.decorators.cache import never_cache



def home(request):
    return render(request,'home.html')
    


def signup(request):
    if request.method == 'POST':
        form = CitoyenCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
             # Crée un profil Citoyen pour l'utilisateur
            Citoyen.objects.create(user=user)
            messages.success(request, "Inscription réussie ! Connectez-vous maintenant.")
            return redirect('login')  # Redirige vers la page de connexion
        else:
            messages.error(request, "Erreur lors de l'inscription.")
    else:
        form = CitoyenCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('admin:index')  # Redirection pour les superutilisateurs
                elif user.role == 'citoyen':
                    return redirect('espace_personnel')  # Redirection pour les citoyens
                elif user.role == 'administration':
                    return redirect('gestion_signalements')  # Redirection pour l'administration
                else:
                    messages.error(request, "Rôle non reconnu.")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Formulaire invalide.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def signaler_probleme(request):
    if not hasattr(request.user, 'citoyen'):
        return redirect('login')  # Redirige vers la page de création du citoyen si ce n'est pas le cas

    if request.method == 'POST':
        form = SignalementForm(request.POST,request.FILES)
        if form.is_valid():
            signalement = form.save(commit=False)
            signalement.citoyen = request.user.citoyen  # On lie le signalement au citoyen connecté
            # Récupérer les coordonnées GPS depuis le formulaire
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            
            # Vérifie si les valeurs existent avant d'enregistrer
            if latitude and longitude:
                signalement.latitude = latitude
                signalement.longitude = longitude

            print(f"Latitude enregistrée : {signalement.latitude}")
            print(f"Longitude enregistrée : {signalement.longitude}")

            signalement.save()
            return redirect('signalement_confirmation')
    else:
        form = SignalementForm()
    
    return render(request, 'signalement_form.html', {'form': form})




@login_required
def verification(request):
   

    signalements = Signalement.objects.filter(citoyen=request.user.citoyen)
    return render(request, 'verifier.html', {'signalements': signalements})


def espace_personnel(request):
   
    return render(request,'monEspace.html')






def signalement_confirmation(request):
    return render(request, 'signalement_confirmation.html')

@login_required
def gestion_signalements(request):
    if request.user.role == 'administration':
        signalements = Signalement.objects.all()  # L'administration voit tous les signalements
    elif request.user.role == 'service_technique':
        signalements = Signalement.objects.filter(service_technique=request.user.service_technique)  # Le service technique ne voit que ses signalements
    else:
        signalements = Signalement.objects.filter(citoyen=request.user.citoyen)  # Le citoyen ne voit que ses propres signalements

    return render(request, 'gestion_signalements.html', {'signalements': signalements})
#@login_required
@never_cache
def changer_statut(request, signalement_id):
    signalement = get_object_or_404(Signalement, id=signalement_id)
    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        signalement.statut = nouveau_statut
        signalement.save()
        messages.success(request, f"Le statut du signalement a été mis à jour : {nouveau_statut}.")
        return redirect('gestion_signalements')
    return render(request, 'changer_statut.html', {'signalement': signalement})