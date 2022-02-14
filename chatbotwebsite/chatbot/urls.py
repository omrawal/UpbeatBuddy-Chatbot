from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.loginPage, name='login'),
    # TODO create a chatpage
    path('chatpage/', views.chatPage, name='chatpage'),
    # path('test', views.testpage, name='test'),
    path('profile/', views.profilePage, name='profile'),
    path('logout/', views.logoutPage, name='logout'),
    # path('register', views.registerpage, name='register'),
]
