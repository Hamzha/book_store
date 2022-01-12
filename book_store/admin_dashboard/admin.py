from django.contrib import admin

# Register your models here.
from book_store.admin_dashboard.models import Book, Cart
from book_store.user.models import User

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Cart)
