from glob import glob
from json import dump, dumps
from .forms import ChatbotUserForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserScore, ChatbotUser
from datetime import datetime
import pytz
from requests.exceptions import ConnectionError
import requests




CHATS = []  # list of tuples (user_query,bot_response)
# External or default URL goes here
CHATBOT_URL = 'http://localhost:5000/'
# CHATBOT_URL = 'http://localhost:5200/'
SENTIMENT_URL = 'http://localhost:5500/'
# SENTIMENT_URL = 'http://localhost:5300/'

# New Analysis data
DataObj=None

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
    response = requests.post(url=CHATBOT_URL, params={
                             'userQuery': str(userQuery)})
    responseJson = response.json()
    res = (responseJson['user_query'],
           responseJson['chatbot_response'],
           datetime.now(pytz.timezone('Asia/Kolkata')
                        ).strftime("%d-%m-%Y %H:%M:%S"),
           )
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
        # the Post request is to register a new user
        if('register' in request.POST):
            form1 = UserCreationForm(data=request.POST)
            form2 = ChatbotUserForm(request.POST)
            if (form1.is_valid() and form2.is_valid()):
                print("Saving form1 .................", form1.save())
                username = form1.cleaned_data['username']
                password = form1.cleaned_data['password1']
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
        context = {'form1': form1, 'form2': form2, 'form3': form3}
        return render(request, "login.html", context)


@login_required(login_url='login')
def chatPage(request):
    global CHATS
    global DataObj
    sentiments = None
    if request.method == 'POST':
        if('Send' in request.POST):
            print("User sent ->>>", request.POST.get('userquery'))
            userQuery = request.POST.get('userquery')
            chat = getChatbotResponse(userQuery=userQuery)
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
            DataObj=scoreObj
            return redirect('profile')


    activate = False
    if(len(CHATS) > 2):
        activate = True
    context = {'userdata': [request], 'chats': CHATS,
               'sentiments': sentiments, 'activate': activate, 'now': datetime.now(pytz.timezone('Asia/Kolkata')
                                                                                   ).strftime("%d-%m-%Y %H:%M:%S"), }
    return render(request, "chatpage.html", context=context)


@login_required(login_url='login')
def profilePage(request):
    global DataObj
    
    current = ChatbotUser.objects.get(user=request.user)
    scoreobj = UserScore.objects.filter(
        owner=current)

    print(len(scoreobj))

    context = {'newUser': True, 'scores': [('score =', 0, ' pos = ',
                                            0, ' neg = ', 0, ' date= ', "No Date")], 'xValues': [0], 'yValues': [
        0], 'posVal': 0, 'negVal': 0, 'avgScore': 0, 'age': current.age, 'email': current.email}
    if(len(scoreobj) != 0):
        userScoreData = []
        xValues = []  # date time
        yValues = []  # score
        posValues = []  # positive values
        negValues = []  # negative values

        for scr in scoreobj:
            k = ('score =', scr.score, ' pos = ',
                 scr.posCount, ' neg = ', scr.negCount, ' date= ', scr.updatedAt.strftime(
                     "%d/%m/%Y - %H:%M:%S"))
            xValues.append(int(scr.updatedAt.strftime(
                "%d")+scr.updatedAt.strftime(
                "%m")+scr.updatedAt.strftime(
                "%Y")))
            yValues.append(int(scr.score*100))
            posValues.append(scr.posCount)
            negValues.append(scr.negCount)
            userScoreData.append(k)
        context = {'newUser': False, 'scores': userScoreData, 'xValues': xValues, 'yValues': yValues, 'posVal': sum(
            posValues), 'negVal': sum(negValues), 'avgScore': round(sum(yValues)/len(yValues), 2), 'age': current.age, 'email': current.email}
    if(DataObj!=None):
        context['dataObj']=DataObj
        DataObj=None
    else:
        context['dataObj']=None

    return(render(request, "profile.html", context=context))


def logoutPage(request):
    logout(request)
    global CHATS
    global DataObj
    DataObj=None
    CHATS = []
    return render(request, 'logout.html')


@login_required(login_url='login')
def linkPage(request):
    chatbot_url = getChatbotUrl()
    sentiment_url = getSentimentUrl()
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

