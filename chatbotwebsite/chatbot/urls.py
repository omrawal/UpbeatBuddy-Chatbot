from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.loginPage, name='login'),
    path('chatpage/', views.chatPage, name='chatpage'),
    path('profile/', views.profilePage, name='profile'),
    path('logout/', views.logoutPage, name='logout'),
    path('linkpage/', views.linkPage, name='linkpage'),
]
