from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User



class ChatForm(forms.Form):
    message = forms.CharField(label='رسالتك', max_length=1000)


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        

class ChangeEmailUsername(forms.ModelForm):
    verification_code = forms.CharField(max_length=6, required=False, label='Verification Code')
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeEmailUsername, self).__init__(*args, **kwargs)
        
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
        email = self.cleaned_data.get("email")
        if email and self.user and email == self.user.email:
            return email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")
        email = self.cleaned_data['email']
        domain = email.split('@')[1]

        if domain not in self.ALLOWED_DOMAINS:
            raise forms.ValidationError(_("Email is not allowed"))

        return email



