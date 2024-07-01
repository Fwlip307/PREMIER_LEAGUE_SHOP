from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class Registro(UserCreationForm):
    first_name = forms.CharField(max_length=20, help_text="Ingrese su nombre")
    last_name = forms.CharField(max_length=20, help_text="Ingrese su apellido")
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")
        
class LoginForm(AuthenticationForm):
    class Meta:
        fields = ("username", "password")
        
class PagoForm(forms.Form):
    username = forms.CharField(max_length=100)
    total = forms.DecimalField()
