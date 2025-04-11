#<!-- filepath: d:\Desktop\fotoblog\fotoblog\blog\templates\blog\forms.py -->

from django import forms
from .models import Jante

class JanteForm(forms.ModelForm):
    class Meta:
        model = Jante
        fields = ['part_number', 'serial_number', 'support', 'category']  # Champs visibles dans le formulaire