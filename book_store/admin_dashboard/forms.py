from django import forms
from django.forms import widgets

from .models import Book

GENRE = [
    ('Action and Adventure', 'Action and Adventure'),
    ('Classics', 'Classics'),
    ('Comic Book or Graphic Novel', 'Comic Book or Graphic Novel'),
    ('Detective and Mystery', 'Detective and Mystery'),
    ('Fantasy', 'Fantasy'),
    ('Historical Fiction', 'Historical Fiction'),
    ('Horror', 'Horror'),
    ('Literary Fiction', 'Literary Fiction'),
    ('romance', 'Romance'),
    ('Science Fiction (Sci-Fi)', 'Science Fiction (Sci-Fi)'),
    ('Short Stories', 'Short Stories'),
    ('Suspense and Thrillers', 'Suspense and Thrillers'),
    ('Biographies and Autobiographies', 'Biographies and Autobiographies'),
    ('Cookbooks', 'Cookbooks'),
    ('Essays', 'Essays'),
    ('History', 'History'),
    ('Memoir', 'Memoir'),
    ('Poetry', 'Poetry'),
    ('Self_Help', 'Self-Help'),
    ('True Crime', 'True Crime')
]

BOOK_STATUS = [
    ('PENDING', 'PENDING'),
    ('NOT AVAIlABLE', 'NOT AVAIlABLE'),
    ('AVAILABLE', 'AVAILABLE')
]


class add_book_form(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    year_of_publish = forms.DateField(required=False, widget=widgets.DateInput(attrs={'type': 'date'}))
    no_of_pages = forms.IntegerField(required=False)

    genre = forms.CharField(widget=forms.Select(choices=GENRE))
    price = forms.FloatField(required=True)
    author = forms.CharField(max_length=100, required=True)
    book_status = forms.CharField(max_length=100, initial='Pending', required=True,widget=forms.Select(choices=BOOK_STATUS))
    cover_photo = forms.ImageField(required=False)

    class Meta:
        model = Book
        fields = ('title', 'year_of_publish', 'no_of_pages', 'genre', 'price', 'author', 'book_status', 'cover_photo')
