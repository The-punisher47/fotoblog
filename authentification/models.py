#<!-- filepath: d:\Desktop\fotoblog\fotoblog\authentification\models.py->
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )

    profile_photo = models.ImageField(upload_to='profile_photos/', verbose_name='Photo de profil', blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle', default=SUBSCRIBER)


class Jante(models.Model):
    # ... vos champs existants ...
    
    def update_ndi_values(self):
        """Met à jour dernier_ndi et prochain_ndi en fonction de nombre_de_deposes"""
        depose_count = self.nombre_de_deposes
        
        if depose_count >= 60:
            self.dernier_ndi = 60
            self.prochain_ndi = "HS"
        else:
            # Exemple de logique de calcul - à adapter selon vos besoins
            intervals = {
                0: (0, 5),
                5: (5, 10),
                10: (10, 15),
                # ... ajoutez tous vos intervalles ...
                55: (55, 60)
            }
            
            for last, next in intervals.values():
                if depose_count == last:
                    self.dernier_ndi = last
                    self.prochain_ndi = next
                    break
