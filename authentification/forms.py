#<!-- filepath: d:\Desktop\fotoblog\fotoblog\authentification\forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

class LoginForm(forms.Form):
    username=forms.CharField(max_length=63,label='nom dutilisateur')
    password=forms.CharField(max_length=63,widget=forms.PasswordInput,label='mot de pass')


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des messages d'aide
        self.fields['username'].help_text = "150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement."
        self.fields['password1'].help_text = """
            <ul>
                <li>Votre mot de passe ne peut pas être trop similaire à vos autres informations personnelles.</li>
                <li>Votre mot de passe doit contenir au moins 8 caractères.</li>
                <li>Votre mot de passe ne peut pas être un mot de passe couramment utilisé.</li>
                <li>Votre mot de passe ne peut pas être entièrement numérique.</li>
            </ul>
        """
        self.fields['password2'].help_text = "Entrez le même mot de passe que précédemment, pour vérification."