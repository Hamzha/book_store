from django import forms
from django.forms import DateField

from . import models


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    email = forms.EmailField(label="E-Mail Address", widget=forms.EmailInput, required=True)
    username = forms.CharField(label="Username", widget=forms.TextInput, required=True)
    first_name = forms.CharField(label="First name ", widget=forms.TextInput, required=False)
    last_name = forms.CharField(label="Last name ", widget=forms.TextInput, required=False)
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput, required=False)

    class Meta:
        model = models.User
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

from django import forms
from django.forms import DateField

from . import models

