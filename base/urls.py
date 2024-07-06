from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('form', views.form, name='form'),
    path('moreinfo', views.moreinfo, name='moreinfo'),
    path('profile', views.profile, name='profile'),
    path('description/<int:Food_ID>/', views.description, name='description')
]