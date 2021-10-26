from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="user-login"),
    path('logout', views.logout_view, name="user-logout"),

    path('signup', views.signup, name="user-signup"),
    path('dashboard', views.dashboard, name='user-dashboard'),
    path('product_detail/<int:product_id>', views.product_detail, name='user-product-detail'),

    path('book_reader/<int:book_id>/<int:page_number>', views.booK_reader, name='user-read-book'),
    path('get_book/<int:book_id>', views.get_book, name='user-get-book'),

    path('save_bookmark/<int:book_id>/<int:page_num>', views.save_bookmark, name='user-bookmark-save'),
    path('remove_bookmark/<int:book_id>/<int:page_num>', views.remove_bookmark, name='user-bookmark-save'),
    path('save_quick_note/<int:book_id>/<int:page_num>', views.save_quick_notes, name='user-quick-notes'),
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
    path('update_Profile', views.user_profile_update, name = 'user_profile_update'),

    path('review_product/<int:book_id>', views.review_book, name= 'user_review_book'),
    path('review_save/<int:book_id>', views.review_save_book, name='user-save-review'),

    path('wishlist', views.wishlist, name='user_wishlist'),

    path('deals_discounts', views.deal_discounts, name= 'user_deals_discount'),
    path('vouchers', views.voucher_list, name='user_voucher'),

    path('check_voucher', views.voucher_check, name='user_check_voucher'),
    path('attempt_quiz/<int:book_id>', views.attempt_quiz, name='user_attempt_quiz'),
    path('check_answer', views.check_answer, name='user_check_answer')
]
