from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from book_store.user.models import Mode, User
import datetime


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
    book_mode = models.ForeignKey(Mode, on_delete=models.CASCADE, blank=True, null=True)
    summary = models.TextField(max_length=500, default='Not Available')
    adult_mode = models.BooleanField(default=False)
    free_book = models.BooleanField(default=False)
    audio = models.FileField(null=True, blank=True, upload_to='books', default='images/not-available.png')
    best_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BookAudio(models.Model):
    audio_id = models.AutoField(primary_key=True)
    audio = models.FileField(null=True, blank=True, upload_to='books', default='images/not-available.png')
    book = models.ManyToManyField(Book, null=True)


class Voucher(models.Model):
    voucher_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200, blank=False, null=False)
    credit = models.IntegerField(null=False, blank=False)
    code = models.CharField(default='', max_length=10)


class VoucherUser(models.Model):
    voucher_user_id = models.AutoField(primary_key=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_type = models.CharField(max_length=100)
    quiz_question_statement = models.CharField(max_length=1000)
    quiz_option_1 = models.CharField(max_length=200)
    quiz_option_2 = models.CharField(max_length=200)
    quiz_option_3 = models.CharField(max_length=200)
    quiz_option_4 = models.CharField(max_length=200)
    quiz_answer = models.CharField(max_length=200, default='')
    quiz_book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)


class QuizUser(models.Model):
    quiz_user_id = models.AutoField(primary_key=True)
    quiz_user_user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_user_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_user_option = models.CharField(max_length=20)


class QuizBook(models.Model):
    quiz_book_id = models.AutoField(primary_key=True)
    quiz_book_score = models.IntegerField()
    quiz_book_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_book_book = models.ForeignKey(Book, on_delete=models.CASCADE)


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_text = models.TextField(max_length=500, default='')
    review_date = models.DateField(default=datetime.datetime.now)
    review_rate = models.IntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])


class Deal(models.Model):
    deal_id = models.AutoField(primary_key=True)
    deal_title = models.TextField(max_length=500, default='')
    deal_valid_upto = models.DateField(default=datetime.datetime.now)
    deal_percentage = models.FloatField(default=00)
    deal_book = models.ManyToManyField(Book)
