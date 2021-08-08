from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="user-login"),
    path('registration', views.register, name="user-register")
]
