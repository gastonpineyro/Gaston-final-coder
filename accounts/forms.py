from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from blog_config.form_mixins import BootstrapFormMixin

from .models import Perfil


class RegistroForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UsuarioForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        labels = {"first_name": "Nombre", "last_name": "Apellido", "email": "Email"}


class PerfilForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["avatar", "biografia"]
        labels = {"avatar": "Imagen de perfil", "biografia": "Biografía"}
        widgets = {"biografia": forms.Textarea(attrs={"rows": 4})}


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass
