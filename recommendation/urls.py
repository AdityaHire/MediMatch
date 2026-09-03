from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.recommend, name='recommend'),
    path('results/', views.results, name='results'),
    path('history/', views.history, name='history'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]
