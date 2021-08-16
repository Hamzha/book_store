from django import forms
from django.forms import widgets

from .models import Book
from ..user.models import User

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

BOOK_TYPE = [
    ('PDF', 'PDF'),
    ('AUDIO', 'AUDIO')
]


class add_book_form(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    year_of_publish = forms.DateField(required=False, widget=widgets.DateInput(attrs={'type': 'date'}))
    no_of_pages = forms.IntegerField(required=False)

    genre = forms.CharField(widget=forms.Select(choices=GENRE))
    price = forms.FloatField(required=True)
    author = forms.CharField(max_length=100, required=True)
    book_status = forms.CharField(max_length=100, initial='Pending', required=True,
                                  widget=forms.Select(choices=BOOK_STATUS))
    cover_photo = forms.ImageField(required=True)
    book_type = forms.CharField(required=True, widget=forms.Select(choices=BOOK_TYPE))
    file = forms.FileField(required=True)

    class Meta:
        model = Book
        fields = ('title', 'year_of_publish', 'no_of_pages', 'genre', 'price', 'author', 'book_status', 'cover_photo',
                  'book_type', 'file')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, required=True)

    email = forms.EmailField(label="E-Mail Address", widget=forms.EmailInput, required=True)
    username = forms.CharField(label="Username", widget=forms.TextInput, required=True)
    first_name = forms.CharField(label="First name ", widget=forms.TextInput, required=False)
    last_name = forms.CharField(label="Last name ", widget=forms.TextInput, required=False)
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}),
                                    required=False)

    class Meta:
        model = User
        fields = ('email',
                  'username',
                  'first_name', 'last_name', 'date_of_birth', 'password', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2
