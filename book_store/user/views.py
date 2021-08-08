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


@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login_user(request, user)
            if user.is_admin:
                return redirect('admin-home')

            return JsonResponse({'Login': 'Pass'})
        else:
            return render(request, 'user/login.html', {'error': "Please enter correct credentials"})

    return render(request, 'user/login.html', {})


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
