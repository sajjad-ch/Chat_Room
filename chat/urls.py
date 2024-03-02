from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('search', views.search_friend, name='search'),
    path('addfriend/<str:username>', views.add_friend, name='addfriend'),
    path("<str:username>", views.chat, name="chat"),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
]