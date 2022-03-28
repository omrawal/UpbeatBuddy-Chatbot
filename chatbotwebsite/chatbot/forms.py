from dataclasses import fields
from pyexpat import model
from django import forms
from .models import ChatbotUser, UserScore, User


class ChatbotUserForm(forms.ModelForm):
    class Meta:
        model = ChatbotUser
        # fields = '__all__'
        # fields = ('age', 'gender', 'isStudent', 'username',
        #           'password', 'firstname', 'lastname', 'email')
        fields = ('email', 'age',
                  #  'gender', 'isStudent'
                  )
        labels = {
            "email": "email",
            "age": "age",
            # "gender": "gender",
            # "isStudent": "isStudent",
        }


class UserScoreForm(forms.ModelForm):
    class Meta:
        model = UserScore
        fields = '__all__'
        # fields = ('age', 'gender', 'isStudent')
