from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="user-login"),
    path('signup', views.signup, name="user-signup"),
    path('dashboard', views.dashboard, name='user-dashboard'),
    path('product_detail/<int:product_id>', views.product_detail, name='user-product-detail'),

    path('book_reader/<int:book_id>/<int:page_number>', views.booK_reader, name='user-read-book'),
    path('get_book/<int:book_id>', views.get_book, name='user-get-book'),

    path('save_bookmark/<int:book_id>/<int:page_num>', views.save_bookmark, name='user-bookmark-save'),
    path('remove_bookmark/<int:book_id>/<int:page_num>', views.remove_bookmark, name='user-bookmark-save'),
    path('save_quick_note/<int:book_id>/<int:page_num>', views.save_quick_notes, name='user-quick-notes'),
    path('get_bookmark/<int:book_id>', views.get_bookmark, name='user-bookmark'),
    path('get_quick_notes', views.get_quick_notes, name='user-quick-notes'),
    path('set_wishlist/<int:book_id>', views.set_wishlist, name='user-set-wishlist'),
    path('remove_wishlist/<int:book_id>', views.remove_wishlist, name='user-remove-wishlist'),
    path('add_to_cart/<int:book_id>', views.add_to_cart, name='user-add-to-cart'),
    path('set_cart', views.set_cart, name='user-set-cart'),
    path('cart', views.cart, name='user-cart'),
    path('cart_payment', views.cart_payment, name='user-cart-payment'),
    path('user_portal', views.user_portal, name='user-portal')

]
