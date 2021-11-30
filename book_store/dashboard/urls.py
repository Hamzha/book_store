from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="user-login"),
    path('logout', views.logout_view, name="user-logout"),

    path('signup', views.signup, name="user-signup"),
    path('dashboard', views.dashboard, name='user-dashboard'),
    path('product_detail/<int:product_id>', views.product_detail, name='user-product-detail'),

    path('book_reader/<int:book_id>/<int:page_number>', views.booK_reader, name='user-read-book'),
    path('book_listen/<int:book_id>', views.booK_listen, name='user-listen-book'),
    path('book_listen_chapter/<int:book_id>/<int:chapter>', views.booK_listen_chapter, name='user-listen_chapter-book'),

    path('get_book/<int:book_id>/<int:chapter_id>', views.get_book, name='user-get-book'),

    path('save_bookmark/<int:book_id>/<int:page_num>', views.save_bookmark, name='user-bookmark-save'),

    path('remove_bookmark/<int:book_id>/<int:page_num>', views.remove_bookmark, name='user-bookmark-save'),
    path('save_quick_note/<int:book_id>/<int:page_num>', views.save_quick_notes, name='user-save-quick-notes'),
    path('get_bookmark/<int:book_id>', views.get_bookmark, name='user-bookmark'),

    path('get_quick_notes/<int:book_id>', views.get_quick_notes, name='user-quick-notes'),
    path('set_wishlist/<int:book_id>', views.set_wishlist, name='user-set-wishlist'),
    path('remove_wishlist/<int:book_id>', views.remove_wishlist, name='user-remove-wishlist'),
    path('add_to_cart/<int:book_id>', views.add_to_cart, name='user-add-to-cart'),
    path('set_cart', views.set_cart, name='user-set-cart'),
    path('cart', views.cart, name='user-cart'),
    path('checkout', views.checkout, name='user-checkout'),
    path('cart_payment', views.checkout, name='user-cart-payment'),
    path('payment_final', views.cart_payment, name='user-payment-final'),
    path('user_profile', views.user_profile, name='user-profile'),
    path('update_Profile', views.user_profile_update, name='user_profile_update'),

    path('review_product/<int:book_id>', views.review_book, name='user_review_book'),
    path('review_save/<int:book_id>', views.review_save_book, name='user-save-review'),

    path('wishlist', views.wishlist, name='user_wishlist'),
    path('wishlist/<str:sort>', views.wishlist_sort, name='user_wishlist_sort'),

    path('deals_discounts', views.deal_discounts, name='user_deals_discount'),
    path('vouchers', views.voucher_list, name='user_voucher'),

    path('check_voucher', views.voucher_check, name='user_check_voucher'),
    path('attempt_quiz/<int:book_id>', views.attempt_quiz, name='user_attempt_quiz'),
    path('check_answer', views.check_answer, name='user_check_answer'),

    path('user_author_menu', views.user_author_menu, name='user_author_menu'),
    path('user_author_add_book', views.user_author_add_book, name='user_author_add_book'),
    path('user_delete_book/<int:book_id>', views.user_delete_book, name='user_delete_book'),
    path('user_genre/<str:genre>', views.user_get_genre_book, name='user-genre-book'),
    path('user_best_book', views.user_get_best_book, name='user-best-book'),
    path('user_audio_book', views.user_get_audio_book, name='user-audio-book'),
    path('pdf_book', views.user_get_pdf_book, name='user-pdf-book'),
    path('search_book/<str:search>', views.user_search_book, name='user_search_book'),
    path('filter_book/', views.user_filter_book, name='user_filter_book'),

    path('check_mail', views.send_mail),
    path('cart_update', views.update_cart),
    path('remove_cart/<int:book_id>', views.remove_cart, name='user-remove-cart'),

    path('query_feedback', views.query_feedback, name='user_query_feedback'),
    path('query_feedback_list', views.query_feedback_list, name='user_query_feedback_list'),

]
