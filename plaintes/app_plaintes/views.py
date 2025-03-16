from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import CitoyenForm, SignalementForm, LoginForm
from .models import Signalement



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Tentative de connexion avec username={username}, password={password}")  # De
            
            user = authenticate(request, username=username, password=password)
            print("------------------------------------")
            print(user)
            print("------------------------------------")
            
            if user is not None:
                print(f"Utilisateur trouvé : {user.username}, rôle : {user.role}")  # Debug
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('admin:index')  # Redirection pour les superutilisateurs
                elif user.role == 'citoyen':
                    return redirect('signaler_probleme')  # Redirection pour les citoyens
                else:
                    print("Aucun utilisateur trouvé ou mot de passe incorrect.") 
                    messages.error(request, "Rôle non reconnu.")
                    
            else:
                print("Formulaire invalide. Erreurs :", form.errors)  # Debug
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Formulaire invalide.")
            print("la belle")
            print("Formulaire invalide. Erreurs :", form.errors)

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def signaler_probleme(request):
    if not hasattr(request.user, 'citoyen'):
        return redirect('creer_citoyen')  # Redirige vers la page de création du citoyen si ce n'est pas le cas

    if request.method == 'POST':
        form = SignalementForm(request.POST)
        if form.is_valid():
            signalement = form.save(commit=False)
            signalement.citoyen = request.user.citoyen  # On lie le signalement au citoyen connecté
            signalement.save()
            return redirect('signalement_confirmation')
    else:
        form = SignalementForm()
    
    return render(request, 'signalement_form.html', {'form': form})

@login_required
def creer_citoyen(request):
    if request.method == 'POST':
        form = CitoyenForm(request.POST)
        if form.is_valid():
            citoyen = form.save(commit=False)
            citoyen.user = request.user  # Lier le citoyen à l'utilisateur connecté
            citoyen.save()
            return redirect('signaler_probleme')
    else:
        form = CitoyenForm()

    return render(request, 'creer_citoyen.html', {'form': form})

def signalement_confirmation(request):
    return render(request, 'signalement_confirmation.html')

@login_required
def gestion_signalements(request):
    signalements = Signalement.objects.all()  # L'administration peut voir tous les signalements
    return render(request, 'gestion_signalements.html', {'signalements': signalements})

@login_required
def changer_statut(request, signalement_id):
    signalement = get_object_or_404(Signalement, id=signalement_id)
    if request.method == 'POST':
        signalement.statut = request.POST['statut']
        signalement.save()
        return redirect('gestion_signalements')
    return render(request, 'changer_statut.html', {'signalement': signalement})