from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="admin-home"),
    path('logout', views.logout_view, name="admin-logout"),

    path('add_book', views.add_book, name="admin-add-book"),
    path('edit_book/<int:book_id>', views.edit_book, name='admin-edit-book'),
    path('list_book', views.list_book, name='admin-list-book'),
    path('delete_book/<int:book_id>', views.delete_book, name='admin-delete-book'),

    path('add_user', views.add_user, name='admin-add-user'),
    path('list_user', views.list_user, name='admin-list-user'),
    path('edit_user/<int:user_id>', views.edit_user, name='admin-edit-user'),
    path('delete_user/<int:user_id>', views.delete_user, name='admin-delete-user'),
    path('make_author_user/<int:user_id>', views.make_author_user, name='admin-make-author-user'),
    path('make_admin_user/<int:user_id>', views.make_admin_user, name='admin-make_admin_user'),

    path('add_user_mode', views.add_mode, name='admin-add-user-mode'),
    path('list_user_mode', views.list_user_mode, name='admin-list-user-mode'),
    path('delete_mode/<int:mode_id>', views.delete_mode, name='admin-mode-user'),
    path('edit_user_mode/<int:mode_id>', views.edit_user_mode, name='admin-edit-user-mode'),

    path('add_deal_voucher', views.add_deal_voucher, name='admin-add-deal-voucher'),
    path('list_deal_voucher', views.list_deal_voucher, name='admin-list-deal-voucher'),
    path('edit_deal_voucher/<int:deal_voucher_id>', views.edit_deal_voucher, name='admin-edit-deal-voucher'),
    path('delete_deal_voucher/<int:deal_voucher_id>', views.delete_deal_voucher, name='admin-delete-deal-voucher'),

    path('add_user_deal_voucher', views.add_user_deal_voucher, name='admin-add-user-deal-voucher'),
    path('list_user_deal_voucher', views.list_user_deal_voucher, name='admin-list-user-deal-voucher'),
    path('delete_user_deal_voucher/<int:deal_voucher_user_id>', views.delete_user_deal_voucher,
         name='admin-delete-deal-voucher-user-id'),
    path('admin_edit_user_deal_voucher/<int:deal_voucher_user_id>', views.admin_edit_user_deal_voucher,
         name='admin-edit-user-deal-voucher'),

    path('add_quiz', views.add_quiz, name='admin-add-quiz'),
    path('list_quiz', views.list_quiz, name='admin-list-quiz'),
    path('save_game', views.save_game, name='admin-save-game'),
    path('save_mcqs', views.save_mcqs, name='admin-save-mcqs'),
    path('save_question', views.save_question, name='admin-save-question'),

    path('add_deal', views.add_deal , name= 'admin-add-deal'),
    path('list_deal', views.list_deal, name='admin-list-deal'),
    path('save_deal', views.save_deal, name='admin-save-deal'),
    path('delete_deal/<int:deal_id>', views.delete_deal, name='admin_delete_deal'),

    path('delete_quiz/<int:quiz_id>', views.delete_quiz, name='admin_delete_quiz'),

    path('check_mail',views.test_mail)
    # path('delete_user_deal_voucher/<int:deal_voucher_user_id>', views.delete_user_deal_voucher,
    #      name='admin-delete-deal-voucher-user-id'),
    # path('admin_edit_user_deal_voucher/<int:deal_voucher_user_id>', views.admin_edit_user_deal_voucher,
    #      name='admin-edit-user-deal-voucher')
    #
    # path('delete_deal_voucher/<int:deal_voucher_id>', views.delete_deal_voucher, name='admin-delete-deal-voucher'),

]
