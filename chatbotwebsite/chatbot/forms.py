from dataclasses import fields
from pyexpat import model
from django import forms
from .models import ChatbotUser, UserScore, User


class ChatbotUserForm(forms.ModelForm):
    class Meta:
        model = ChatbotUser
        fields = ('email', 'age',)
        labels = {
            "email": "email",
            "age": "age",
        }


class UserScoreForm(forms.ModelForm):
    class Meta:
        model = UserScore
        fields = '__all__'
