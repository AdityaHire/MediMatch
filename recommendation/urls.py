from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recommend/', views.recommend, name='recommend'),
    path('results/', views.results, name='results'),
    path('history/', views.history, name='history'),
]
