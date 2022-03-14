from requests.exceptions import ConnectionError
import requests
CHATBOT_URL = 'http://localhost:5000/'
# CHATBOT_URL = 'http://localhost:5200/'
SENTIMENT_URL = 'http://localhost:5500/'
# SENTIMENT_URL = 'http://localhost:5300/'


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


# print(getSentimentalResponse(['I am so sad', "All the misfortunes are given to me", "This was a very bad day",
#                               "I was in an accident and now I have to pay for my car's reapirs",
#                               " I am already short on money and I am not sure if I will even be able to pay rent next week",
#                               "Yes Yes Yes Yes YES!!!", "I am so so happy", "Today is the best day", "This is just great", 'I am so sad', "All the misfortunes are given to me", "This was a very bad day"
#                               "I was in an accident and now I have to pay for my car's reapirs. I am already short on money and I am not sure if I will even be able to pay rent next week"]))
