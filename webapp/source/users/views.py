from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import LoginForm, SignUpForm
from .models import *
from learning import models as lm


# Логин юзера
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])  # Аутентификация пользователя
            if user is not None:
                if user.is_active:
                    login(request, user)  # Сразу логиним юзера после регистрации
                    return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


# Логаут юзера
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# Регистрация
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            rp = request.POST
            # Получение данных из формы
            username = rp['username']
            password = rp['password1']
            first_name = rp['first_name']
            last_name = rp['last_name']

            user = authenticate(username=username, password=password)  # Аутентификация юзера

            person = lm.Person()  # Получаем модель человека
            person.user = user  # Связываем ее с юзером
            # Устанавливаем имя и фамилию
            person.first_name = first_name
            person.last_name = last_name
            person.save()

            login(request, user)
            return HttpResponseRedirect('/')

    else:
        form = SignUpForm()
    return render(request, 'users/sign_up.html', {'form': form})
