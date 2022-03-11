from requests.exceptions import ConnectionError
import requests
CHATBOT_URL = 'http://localhost:5000/'
SENTIMENT_URL = 'http://localhost:6000/'


def checkUrl(url):
    try:
        request = requests.get(url)
    except ConnectionError:
        return False
    else:
        return True


def getChatbotResponse(userQuery):
    global CHATBOT_URL
    response = requests.get(
        url=CHATBOT_URL+userQuery)
    responseJson = response.json()
    res = (responseJson['user_query'], responseJson['chatbot_response'])
    return res


def setChatbotUrl(url):
    global CHATBOT_URL
    CHATBOT_URL = url


def setSentimentUrl(url):
    global SENTIMENT_URL
    SENTIMENT_URL = url
