from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from . import forms
from .forms import RegisterForm


def register(request):
    print('called')
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            print('valid')
            user.password = make_password(user.password)
            user.save()
            return render(request, 'user/login.html', {})

        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

            return render(request, 'user/registration.html', {'form': RegisterForm})

    else:
        return render(request, 'user/registration.html', {'form': RegisterForm})
