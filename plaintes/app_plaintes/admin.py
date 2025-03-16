from django.contrib import admin
from .models import CustomUser,Citoyen,Administration,ServiceTechnique,Signalement,Notification



admin.site.register(CustomUser)
admin.site.register(Citoyen)
admin.site.register(Administration,)
admin.site.register(ServiceTechnique)
admin.site.register(Signalement)
admin.site.register(Notification)


# Register your models here.
