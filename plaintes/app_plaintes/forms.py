from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Signalement,CustomUser
from django.contrib.auth.forms import AuthenticationForm



class CitoyenCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'matricule', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'citoyen'  # Définir automatiquement le rôle comme "citoyen"
        if commit:
            user.save()
        return user

class SignalementForm(forms.ModelForm):
    class Meta:
        model = Signalement
        fields = ['type_probleme', 'description', 'adresse_signalement','image', 'video', 'audio']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))