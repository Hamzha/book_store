from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="admin-home"),
    path('add_book', views.add_book, name="admin-add-book"),
    path('edit_book/<int:book_id>', views.edit_book, name='admin-edit-book'),
    path('list_book', views.list_book, name='admin-list-book'),
    path('delete_book/<int:book_id>', views.delete_book, name='admin-delete-book'),
    path('add_user', views.add_user, name='admin-add-user'),
    path('list_user', views.list_user, name='admin-list-user'),
    path('edit_user/<int:user_id>', views.edit_user, name='admin-edit-user'),
    path('delete_user/<int:user_id>', views.delete_user, name='admin-delete-user'),

    # path('registration', views.register, name="user-register")
]

