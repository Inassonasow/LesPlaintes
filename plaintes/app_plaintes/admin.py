from django.contrib import admin
from .models import CustomUser,Citoyen,Administration,ServiceTechnique,Signalement,Notification
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # Configuration spécifique pour l'affichage dans l'admin
    model = CustomUser
    list_display = ['username', 'email', 'matricule', 'role', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'email', 'matricule')}),
        ('Permissions', {'fields': ('role', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'matricule', 'password1', 'password2', 'role'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Citoyen)
admin.site.register(Administration,)
admin.site.register(ServiceTechnique)
admin.site.register(Signalement)
admin.site.register(Notification)


# Register your models here.
