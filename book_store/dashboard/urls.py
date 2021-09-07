from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="user-login"),
    path('dashboard', views.product_detail, name='user-dashboard'),
    path('book_reader/<int:book_id>/<int:page_number>', views.booK_reader, name='user-read-book'),
    path('get_book/<int:book_id>', views.get_book, name='user-get-book'),
    path('save_bookmark/<int:book_id>/<int:page_num>', views.save_bookmark, name='user-bookmark-save')
]
