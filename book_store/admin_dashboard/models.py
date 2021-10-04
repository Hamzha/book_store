from django.db import models

# Create your models here.
from book_store.user.models import Mode, User


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    year_of_publish = models.DateField(blank=True, null=True)
    no_of_pages = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=100)
    price = models.FloatField()
    author = models.CharField(max_length=100)
    book_status = models.CharField(max_length=100, default='Pending')
    cover_photo = models.ImageField(null=True, blank=True, upload_to='images')
    book_type = models.CharField(null=False, blank=False, max_length=100, default='Pending')
    pdf = models.FileField(null=True, blank=True, upload_to='books', default='images/not-available.png')
    audio = models.FileField(null=True, blank=True, upload_to='books', default='images/not-available.png')
    book_mode = models.ForeignKey(Mode, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class DealVoucher(models.Model):
    deal_voucher_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200, blank=False, null=False)
    type = models.CharField(max_length=100, blank=False, null=False)
    credit = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.type


class DealVoucherUser(models.Model):
    deal_voucher_user_id = models.AutoField(primary_key=True)
    deal_voucher = models.ForeignKey(DealVoucher, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    valid_up_to = models.DateField(blank=False, null=False)


class BookMark(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    bookmark_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookmark_user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookmark_page_number = models.IntegerField()
    bookmark_text = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.bookmark_page_number


class QuickNote(models.Model):
    QuickNote_id = models.AutoField(primary_key=True)
    QuickNote_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    QuickNote_user = models.ForeignKey(User, on_delete=models.CASCADE)
    QuickNote_page_number = models.IntegerField()
    QuickNote_text = models.TextField(max_length=200, null=True, blank=True)


class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    wishlist_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    wishlist_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    cart_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_book = models.ManyToManyField(Book)
    payment_status = models.CharField(max_length=200, null=True, blank=True)
    cart_detail = models.CharField(max_length=200, null=True, blank=True)
