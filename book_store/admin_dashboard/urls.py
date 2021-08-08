from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="admin-home"),
    # path('registration', views.register, name="user-register")
]
