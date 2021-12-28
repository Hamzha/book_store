from django import forms
from django.forms import widgets

from .models import Book, Voucher, VoucherUser, QueryFeedback
from ..user.models import User, Mode

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
    ('BOTH', 'BOTH AUDIO AND PDF'),
    ('PDF', 'PDF'),
]

VOUCHER_TYPE = [
    ('TICK CROSS', 'TICK CROSS'),
    ('SNAKE', 'SNAKE'),
    ('Others', 'Others')
]


class book_form(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    year_of_publish = forms.DateField(required=False, widget=widgets.DateInput(attrs={'type': 'date'}))
    no_of_pages = forms.IntegerField(required=False)

    genre = forms.CharField(widget=forms.Select(choices=GENRE))
    price = forms.FloatField(required=True)
    author = forms.CharField(max_length=100, required=True)

    cover_photo = forms.ImageField(required=True)
    book_type = forms.CharField(required=True, widget=forms.Select(choices=BOOK_TYPE))
    pdf = forms.FileField(required=False)
    audio = forms.FileField(required=False)
    adult_mode = forms.BooleanField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    free_book = forms.BooleanField(required=False)
    best_seller = forms.BooleanField(required=False)
    summary = forms.Textarea()

    class Meta:
        model = Book
        fields = (
            'title', 'year_of_publish', 'no_of_pages', 'genre', 'price', 'author', 'adult_mode', 'summary',
            'cover_photo',
            'book_type', 'audio', 'pdf', 'free_book', 'best_seller')


class register_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,min_length=8, required=True)
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


class user_mode_form(forms.ModelForm):
    type = forms.CharField(label="Username", widget=forms.TextInput, required=True)
    book_limit = forms.IntegerField(required=True)

    class Meta:
        model = Mode
        fields = ('type', 'book_limit')


class deal_voucher_form(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=True)
    type = forms.CharField(max_length=100, initial='Tick Cross', required=True,
                           widget=forms.Select(choices=VOUCHER_TYPE))
    credit = forms.IntegerField(required=True, widget=forms.NumberInput)

    class Meta:
        model = Voucher
        fields = ('description', 'type', 'credit')


class user_deal_voucher_form(forms.ModelForm):
    deal_voucher = forms.ModelChoiceField(queryset=Voucher.objects.all(), required=True)
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    valid_up_to = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = VoucherUser
        fields = ('deal_voucher', 'user', 'valid_up_to')


class queryFeedbackForm(forms.ModelForm):
    query_feedback_subject = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}),max_length=100, required=True)
    query_feedback_text = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}), required=True)
    query_feedback_reply = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = QueryFeedback
        fields = ('query_feedback_subject', 'query_feedback_text', 'query_feedback_reply')

