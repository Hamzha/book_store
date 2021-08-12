from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="admin-home"),
    path('add_book', views.add_book, name="admin-add-book"),

    # path('registration', views.register, name="user-register")
]

