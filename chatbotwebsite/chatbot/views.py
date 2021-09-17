from django.shortcuts import render, redirect
from django.http import HttpResponse, request

# Create your views here.


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def chatpage(request):
    return render(request, "chatpage.html")
