from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="user-login"),
    path('dashboard', views.dashboard, name='user-dashboard'),
    path('get_book/<int:book_id>', views.get_book, name='user-get-book')
]
