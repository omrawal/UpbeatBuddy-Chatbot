from .forms import ChatbotUserForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import UserScore, ChatbotUser
from datetime import datetime
from requests.exceptions import ConnectionError
import requests
# Create your views here.

CHATS = []  # list of tuples (user_query,bot_response)
# CHATBOT_URL = 'http://localhost:5000/'
CHATBOT_URL = 'http://localhost:5200/'
# SENTIMENT_URL = 'http://localhost:5500/'
SENTIMENT_URL = 'http://localhost:5300/'


# helper methods

def checkUrl(url):
    try:
        request = requests.get(url)
    except ConnectionError:
        return False
    else:
        return True


def getChatbotResponse(userQuery):
    global CHATBOT_URL
    # response = requests.get(
    #     url=CHATBOT_URL+userQuery)
    response = requests.post(url=CHATBOT_URL, params={
                             'userQuery': str(userQuery)})
    responseJson = response.json()
    res = (responseJson['user_query'], responseJson['chatbot_response'])
    return res


def getSentenceListFromChats(chats):
    sentenceList = []
    for conv in chats:
        sentenceList.append(conv[0])
    return sentenceList


def getSentimentalResponse(sentenceList):
    global SENTIMENT_URL
    response = requests.post(url=SENTIMENT_URL, params={
                             'sentList': str(sentenceList)})
    responseJson = response.json()
    return responseJson


def setChatbotUrl(url):
    global CHATBOT_URL
    CHATBOT_URL = url


def setSentimentUrl(url):
    global SENTIMENT_URL
    SENTIMENT_URL = url


def getChatbotUrl():
    global CHATBOT_URL
    return CHATBOT_URL


def getSentimentUrl():
    global SENTIMENT_URL
    return SENTIMENT_URL


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


@login_required(login_url='login')
def chatPage(request):
    chatbot_url = getChatbotUrl()
    sentiment_url = getSentimentUrl()
    if(checkUrl(chatbot_url) == False or checkUrl(sentiment_url) == False):
        return redirect('linkpage')
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
            # saving the score
            chatbotUserObj = ChatbotUser.objects.get(user=request.user)
            scoreObj = UserScore(owner=chatbotUserObj,
                                 score=sentiments['total_score'],
                                 posCount=sentiments['positive_score'],
                                 negCount=sentiments['negative_score'])
            scoreObj.save()

    activate = False
    if(len(CHATS) > 5):
        activate = True
    context = {'userdata': [request], 'chats': CHATS,
               'sentiments': sentiments, 'activate': activate}
    # print('second-----', CHATS)
    return render(request, "chatpage.html", context=context)


@login_required(login_url='login')
def profilePage(request):
    scoreobj = UserScore.objects.filter(
        owner=ChatbotUser.objects.get(user=request.user))
    print(scoreobj)
    userScoreData = []
    for scr in scoreobj:
        k = ('score =', scr.score, ' pos = ',
             scr.posCount, ' neg = ', scr.negCount, ' date= ', scr.updatedAt.strftime(
                 "%d/%m/%Y - %H:%M:%S"))
        print(k)
        userScoreData.append(k)
    context = {'scores': userScoreData}
    return(render(request, "profile.html", context=context))


def logoutPage(request):
    logout(request)
    global CHATS
    CHATS = []
    return render(request, 'logout.html')


@login_required(login_url='login')
def linkPage(request):
    chatbot_url = getChatbotUrl()
    sentiment_url = getSentimentUrl()
    print('chaturl= ', chatbot_url, ' sentiment_url= ', sentiment_url)
    chatbotAPIStatus = False
    sentimentAPIStatus = False
    if(checkUrl(chatbot_url)):
        chatbotAPIStatus = True
    if(checkUrl(sentiment_url)):
        sentimentAPIStatus = True
    context = {'chatbotAPI': chatbotAPIStatus,
               'sentimentAPI': sentimentAPIStatus}
    if request.method == 'POST':
        newChatbotURL = request.POST.get('chatbotLink')
        newSentimentURL = request.POST.get('sentimentLink')
        if(newChatbotURL is not None and newChatbotURL != ''):
            setChatbotUrl(newChatbotURL)
        if(newSentimentURL is not None and newSentimentURL != ''):
            setSentimentUrl(newSentimentURL)
        return redirect('chatpage')
    return render(request, 'link.html', context=context)

# Test
# Test@123
# Test@gmail.com


# TestUser2
# Test2@999
# TestUser@gmail.com
