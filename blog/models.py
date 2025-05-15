from django.db import models
from django.utils.html import format_html
from django.contrib.auth import get_user_model

class Jante(models.Model):
    part_number = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[('NEZ', 'NEZ'), ('PRINCIPALE', 'PRINCIPALE')])
    serial_number = models.CharField(max_length=100)
    support = models.CharField(max_length=50)
    nombre_de_deposes = models.IntegerField(default=0)
    dernier_ndi = models.IntegerField(default=0)
    prochain_ndi = models.CharField(max_length=10, default="5")
    obs = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.serial_number

    def update_ndi_values(self):
        if self.nombre_de_deposes == 60:
            self.dernier_ndi = 60
            self.prochain_ndi = "HS"
        else:
            intervals = [
                (0, 5), (5, 10), (10, 15), (15, 18), (18, 21), (21, 24),
                (24, 27), (27, 30), (30, 33), (33, 36), (36, 39), (39, 42),
                (42, 45),(45,46), (46, 47), (47, 48), (48, 49), (49, 50), (50, 51),
                (51, 52), (52, 53), (53, 54), (54, 55), (55, 56), (56, 57),(57,58),
                (58, 59), (59, 60)
            ]
            for dernier, prochain in intervals:
                if self.nombre_de_deposes == dernier:
                    self.dernier_ndi = dernier
                    self.prochain_ndi = prochain
                    break
        self.save()

    def check_and_create_notification(self):
        if self.prochain_ndi != "HS" and self.nombre_de_deposes == int(self.prochain_ndi) - 1:
            Notification.objects.create(
                message=f"La jante {self.serial_number} approche de son prochain NDI ({self.prochain_ndi}).",
                is_read=False
            )

class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Création'),
        ('UPDATE', 'Mise à jour'),
        ('DELETE', 'Suppression'),
        ('LOGIN', 'Connexion'),
        ('LOGOUT', 'Déconnexion'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    action_type = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    target_model = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.get_action_type_display()} par {self.user} à {self.timestamp}"