#<!-- filepath: d:\Desktop\fotoblog\fotoblog\authentification\forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



class LoginForm(forms.Form):
    username=forms.CharField(max_length=63,label='nom dutilisateur')
    password=forms.CharField(max_length=63,widget=forms.PasswordInput,label='mot de pass')


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'grade')  # Changé role → grade

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].help_text = "Sélectionnez votre grade dans la liste"