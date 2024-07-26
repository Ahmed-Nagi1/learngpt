from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import re

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _("Username")}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": _("Email")}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Password"), 'autocomplete':"off"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Confirm Password"), 'autocomplete':"off"})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("This username already exists"))
        elif len(username) < 4:
            raise forms.ValidationError(
                _("Please enter a valid username (at least 4 characters)")
            )
        elif len(username) > 14:
            raise forms.ValidationError(
                _("Please enter a valid username (14 characters at most)")
            )
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise forms.ValidationError(_("Please enter a valid username"))

        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")

        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return password2


    ALLOWED_DOMAINS = [
        'gmail.com',
        'yahoo.com',
        'outlook.com',
        'hotmail.com',
        'live.com',
        'aol.com',
        'icloud.com',
        'office365.com',
        'zoho.com'
    ]
    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('@')[1]

        if domain not in self.ALLOWED_DOMAINS:
            raise forms.ValidationError(_("Email is not allowed"))

        return email

