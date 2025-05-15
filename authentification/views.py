from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import forms

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.contrib.auth.forms import PasswordChangeForm


class LoginPageView(View):
    template_name = 'authentification/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def signup_page(request):
    # 🔒 Seuls les superutilisateurs peuvent accéder à l'inscription
    if not request.user.is_superuser:
        return render(request, 'authentification/access_denied.html', {
            'message': "⛔ Accès refusé. Seuls les administrateurs peuvent créer un utilisateur."
        })

    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # tu peux changer vers 'home' ou autre

    return render(request, 'authentification/signup.html', context={'form': form})


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def changer_mot_de_passe(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # évite la déconnexion
            messages.success(request, 'Votre mot de passe a été modifié avec succès.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'authentification/change_password.html', {'form': form})
