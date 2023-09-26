from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegisterForm, MassageForm
# Create your views here.

def index(request):
    form = MassageForm()
    if request.method == 'POST':
        form = MassageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'pages/index.html', {'form':MassageForm})

def contact(request):
    return render(request, 'pages/contact.html')

def home(request):
    return render(request, 'pages/home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, pssword=password)
        if user is not None:
            login(request, user)
            return redirect('pages/home.html')
        else:
            messages.error(request, 'Username or Password is Incorrect')
    return render(request, 'pages/login.html', {})

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'pages/signup.html', {'form':RegisterForm})