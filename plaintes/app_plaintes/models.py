from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group,Permission


# =======================
# Modèles des Acteurs
# =======================

class CustomUser(AbstractUser):
    """Modèle utilisateur personnalisé avec des rôles spécifiques"""
    ROLE_CHOICES = [
        ('citoyen', 'Citoyen'),
        ('administration', 'Administration'),
        ('service_technique', 'Service Technique'),
    ]
   
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    matricule = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    # Dans CustomUser, ajouter:
   

    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Citoyen(models.Model):
    """Modèle pour les citoyens"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="citoyen")
    adresse = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Administration(models.Model):
    """Modèle pour l'administration"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="administration")
    service_responsable = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.service_responsable}"

class ServiceTechnique(models.Model):
    """Modèle pour les services techniques"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="service_technique")
    domaine_intervention = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.domaine_intervention}"


# Modèles des Signalements


class Signalement(models.Model):
    """Modèle pour le signalement des problèmes urbains"""
    TYPE_PROBLEME_CHOICES = [
        ('voirie', 'Problème de voirie'),
        ('eclairage', 'Panne d’éclairage public'),
        ('ordures', 'Accumulation de déchets'),
        ('autre', 'Autre problème'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('resolu', 'Résolu'),
        ('rejete', 'Rejeté'),
    ]

    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name="signalements")
    type_probleme = models.CharField(max_length=50, choices=TYPE_PROBLEME_CHOICES, default='autre')
    description = models.TextField()
    adresse_signalement = models.CharField(max_length=255)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_signalement = models.DateTimeField(auto_now_add=True)
    service_technique = models.ForeignKey(ServiceTechnique, on_delete=models.SET_NULL, null=True, blank=True, related_name="interventions")
    # Champs pour la localisation 📍
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


    # Champs pour les fichiers multimédias
    image = models.ImageField(upload_to='signalements/images/', blank=True, null=True)
    video = models.FileField(upload_to='signalements/videos/', blank=True, null=True)
    audio = models.FileField(upload_to='signalements/audios/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_type_probleme_display()} signalé par {self.citoyen.user.username} - {self.get_statut_display()}"

# =======================
# Notifications et Réponses
# =======================

class Notification(models.Model):
    """Modèle pour les notifications envoyées aux citoyens"""
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name="notifications")
    signalement = models.ForeignKey(Signalement, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    date_notification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.citoyen.user.username}"
# Create your models here.
