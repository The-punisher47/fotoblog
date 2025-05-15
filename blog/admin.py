from django.contrib import admin

# Register your models here.
# admin.py dans ton app `blog`
from django.contrib import admin
from .models import Jante, Notification, ActionLog  # ajoute tous les modèles ici
from authentification.models import User  # Si tu as un User personnalisé

# Exemple de configuration de l'admin pour Jante
@admin.register(Jante)
class JanteAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'category', 'serial_number', 'prochain_ndi')
    search_fields = ('part_number', 'serial_number')
    list_filter = ('category',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('message',)

@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'target_model', 'timestamp')
    list_filter = ('action_type', 'target_model')
    search_fields = ('user__username', 'details')

# Optionnel : enregistrer le User personnalisé
from django.contrib.auth.admin import UserAdmin
from authentification.models import User as CustomUser

admin.site.register(CustomUser, UserAdmin)
