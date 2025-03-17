
from django.urls import path
from .views import signaler_probleme,signalement_confirmation,gestion_signalements,changer_statut,login_view,signup,home,verification,espace_personnel
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', home, name='home'),  # Page d'accueil
    path('signup/', signup, name='signup'),  # URL pour l'inscription
    path('verification/', verification, name='verification'),
    path('espace/', espace_personnel, name='espace_personnel'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signaler/', signaler_probleme,name='signaler_probleme'),                           
    path('confirmation/',signalement_confirmation, name='signalement_confirmation'),
    path('gestion_signalements/', gestion_signalements, name='gestion_signalements'),
    path('changer_statut/<int:signalement_id>/', changer_statut, name='changer_statut'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)