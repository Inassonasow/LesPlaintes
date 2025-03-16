
from django.urls import path
from .views import signaler_probleme,signalement_confirmation,gestion_signalements,changer_statut,creer_citoyen,login_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', login_view, name='login'),
    path('signaler/', signaler_probleme,name='signaler_probleme'),                           
    path('confirmation/',signalement_confirmation, name='signalement_confirmation'),
    path('gestion/',gestion_signalements, name='gestion_signalements'),
    path('changer_statut/<int:signalement_id>/', changer_statut, name='changer_statut'),
    path('creer_citoyen/',creer_citoyen, name='creer_citoyen'),
]