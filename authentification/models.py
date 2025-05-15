#<!-- filepath: d:\Desktop\fotoblog\fotoblog\authentification\models.py->
from django.db import models
from django.contrib.auth.models import AbstractUser


# Remplacer la classe User existante par
class User(AbstractUser):
    GRADE_CHOICES = (
        ('SGT', 'Sergent'),
        ('SCH', 'Sous-chef'),
        ('ADJ', 'Adjudant'),
        ('ADC', 'Adjudant-chef'),
        ('SLT', 'Sous-lieutenant'), 
        ('LT', 'Lieutenant'),
        ('CNE', 'Capitaine'),
        ('CDT', 'Commandant'),
        ('LT-COL', 'Lieutenant-colonel'),
        ('COL', 'Colonel'),
    )
    
    grade = models.CharField(
        max_length=10,
        choices=GRADE_CHOICES,
        verbose_name='Grade',
        default='SGT'
    )
    
    def get_grade_display(self):
        return dict(self.GRADE_CHOICES).get(self.grade, self.grade)