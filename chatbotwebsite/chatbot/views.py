from .forms import ChatbotUserForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def loginPage(request):
    return render(request, "login.html")

# TODO create a chatpage


def chatpage(request):
    return render(request, "login.html")


# Test
# Test@123
# Test@gmail.com


def testpage(request):
    if request.method == 'POST':
        print("Got post")
        form1 = UserCreationForm(request.POST)
        form2 = ChatbotUserForm(request.POST)
        print('#### Form 2 ####', form2)
        if form1.is_valid():
            print("SAving form1 .................", form1.save())
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password1']
            print("Username and password are ->>>", username, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            form2 = ChatbotUserForm(request.POST)
            if(form2.is_valid()):
                obj = form2.save(commit=False)
                obj.user = user
                obj.save()
            else:
                print('form2 not valid')
            return redirect('index')
    else:
        print("Got get")
        form1 = UserCreationForm()
        form2 = ChatbotUserForm()
    # print(form1)
    # print(form2)
    context = {'form1': form1, 'form2': form2}

    # context = {}
    return render(request, "test.html", context)
