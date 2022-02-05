from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ChatbotUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    age = models.PositiveIntegerField()
    gender = models.BooleanField()  # True = male ; False = Female
    isStudent = models.BooleanField()


class UserScore(models.Model):
    owner = models.ForeignKey(ChatbotUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    updatedAt = models.DateTimeField(auto_now=True)
