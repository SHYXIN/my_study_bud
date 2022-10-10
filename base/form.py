from django.forms import ModelForm
from django import forms
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class MyUserCreationFrom(UserCreationForm):
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['name' , 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # fields = ['name', 'hose']
        exclude = ['host', 'participants']
        
class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email']
        # fields = '__all__'