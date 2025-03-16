from django import forms
from .models import Signalement,Citoyen
from django.contrib.auth.forms import AuthenticationForm

class SignalementForm(forms.ModelForm):
    class Meta:
        model = Signalement
        fields = ['type_probleme', 'description', 'adresse_signalement']

class CitoyenForm(forms.ModelForm):
    """Formulaire pour la création du profil Citoyen"""
    class Meta:
        model = Citoyen
        fields = ['adresse']  # Ajouter les champs nécessaires


    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))