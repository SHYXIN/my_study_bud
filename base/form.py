from dataclasses import field
from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # fields = ['name', 'hose']
        exclude = ['host', 'participants']
        
class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']
        # fields = '__all__'