from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# https://stackoverflow.com/questions/48049498/django-usercreationform-custom-fields
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
# https://testdriven.io/blog/django-custom-user-model/


class ChatbotUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True, null=True,)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    STUDENT_CHOICES = (
        ('student', 'Student'),
        ('nostudent', 'Not a Student')
    )
    # True = male ; False = Female
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=20, )
    isStudent = models.CharField(
        choices=STUDENT_CHOICES, max_length=20, )

    def __str__(self) -> str:
        return self.user.username+"__"+str(self.email)


class UserScore(models.Model):
    owner = models.ForeignKey(ChatbotUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.owner.user.username+'__'+str(self.updatedAt)
