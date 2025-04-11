#filepath: d:\Desktop\fotoblog\fotoblog\blog\models.py 
from django.db import models
from django.utils.html import format_html

class Jante(models.Model):
    part_number = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[('NEZ', 'NEZ'), ('PRINCIPALE', 'PRINCIPALE')])
    serial_number = models.CharField(max_length=100)
    support = models.CharField(max_length=50)
    nombre_de_deposes = models.IntegerField(default=0)
    dernier_ndi = models.IntegerField(default=0)
    prochain_ndi = models.CharField(max_length=10, default="5")  # Peut être "HS"
    obs = models.TextField(blank=True, null=True)  # Permet de laisser le champ vide

    def __str__(self):
        return self.serial_number

    def update_ndi_values(self):
        """Met à jour les valeurs de dernier_ndi et prochain_ndi en fonction de nombre_de_deposes."""
        if self.nombre_de_deposes == 60:
            self.dernier_ndi = 60
            self.prochain_ndi = "HS"
        else:
            # Logique pour les autres cas
            intervals = [
                (0, 5), (5, 10), (10, 15), (15, 18), (18, 21), (21, 24),
                (24, 27), (30, 33), (33, 36), (36, 39), (42, 45), (46, 47),
                (47, 48), (48, 49), (49, 50), (50, 51), (51, 52), (52, 53),
                (53, 54), (54, 55), (55, 56), (56, 57), (58, 59), (59, 60)
            ]
            for dernier, prochain in intervals:
                if self.nombre_de_deposes == dernier:
                    self.dernier_ndi = dernier
                    self.prochain_ndi = prochain
                    break
        self.save()

    def action_buttons(self):
        """Génère les boutons Add et Delete pour le tableau."""
        return format_html(
            '<button class="action-button add">Add</button>'
            '<button class="action-button delete">Delete</button>'
        )

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Nouveau champ pour indiquer si la notification est lue

    def __str__(self):
        return self.message