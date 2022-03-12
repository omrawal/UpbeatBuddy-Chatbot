from .forms import ChatbotUserForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .helper_function import getChatbotResponse, getSentimentalResponse
from .helper_function import getSentenceListFromChats
# Create your views here.

CHATS = []  # list of tuples (user_query,bot_response)


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def loginPage(request):
    form1 = None
    form2 = None
    if request.method == 'POST':
        print("Got post")
        print(dict(request.POST.items()))
        # the Post request is to register a new user
        if('register' in request.POST):
            form1 = UserCreationForm(data=request.POST)
            form2 = ChatbotUserForm(request.POST)
            print('#### Form 1 ####', form1)
            print('#### Form 2 ####', form2)
            print("Validity 1 ### ", form1.is_valid())
            print("Validity 2 ### ", form2.is_valid())
            if (form1.is_valid() and form2.is_valid()):
                print("Saving form1 .................", form1.save())
                username = form1.cleaned_data['username']
                password = form1.cleaned_data['password1']
                print("Username and password are ->>>", username, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                form2 = ChatbotUserForm(request.POST)
                obj = form2.save(commit=False)
                obj.user = user
                obj.save()
                # messages.success(request, 'Account created successfully')
                return redirect('profile')
            else:
                return redirect('login')
        # the Post request is to login existing user user
        elif('login' in request.POST):
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                global CHATS
                CHATS = []
                return redirect('profile')
            else:
                print("User not found")
                return redirect('login')
        else:
            print("### unknown Post Request ###")
    # GET request send the forms
    else:
        print("Got get")
        form1 = UserCreationForm()
        form2 = ChatbotUserForm()
        form3 = AuthenticationForm()
        print("#### form 3 ##", form3)
        context = {'form1': form1, 'form2': form2, 'form3': form3}
        return render(request, "login.html", context)

# TODO create a chatpage


@login_required(login_url='login')
def chatPage(request):
    global CHATS
    sentiments = None
    if request.method == 'POST':
        if('send' in request.POST):
            print("User sent ->>>", request.POST.get('userquery'))
            userQuery = request.POST.get('userquery')
            chat = getChatbotResponse(userQuery=userQuery)
            # print('first-----', chat)
            CHATS.append(chat)
        if('Check Emotion' in request.POST):
            print("User tried to check ->>>")
            sentList = getSentenceListFromChats(chats=CHATS)
            sentiments = getSentimentalResponse(sentenceList=sentList)
            print('Sentiments are ->', sentiments)
    activate = False
    if(len(CHATS) > 5):
        activate = True
    context = {'userdata': [request], 'chats': CHATS,
               'sentiments': sentiments, 'activate': activate}
    # print('second-----', CHATS)
    return render(request, "chatpage.html", context=context)


@login_required(login_url='login')
def profilePage(request):
    context = {'userdata': [request]}
    return(render(request, "profile.html"))


def logoutPage(request):
    logout(request)
    global CHATS
    CHATS = []
    return render(request, 'logout.html')

# Test
# Test@123
# Test@gmail.com


# TestUser2
# Test2@999
# TestUser@gmail.com
