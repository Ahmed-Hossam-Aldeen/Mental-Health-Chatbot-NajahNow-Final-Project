from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
]
