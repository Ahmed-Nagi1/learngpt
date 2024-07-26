import requests
from .forms import RegisterForm
from django.conf import settings
from django.views import View
from .authenticate import authenticate_eu
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .tasks import send_confirmation_email
from django.utils.crypto import get_random_string
from .models import Profile


@cache_page(60 * 15)
def redirect_login(request):
    return redirect('login')

def recaptcha(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    return result['success']

class SignUp(CreateView):
    model = User 
    form_class = RegisterForm
    template_name = 'accounts/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('choose')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # if recaptcha(self.request):
        if 1:
            email = form.cleaned_data.get('email').lower()
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    code = get_random_string(length=6, allowed_chars='1234567890')
                    self.request.session['email_confirmation_code'] = code
                    send_confirmation_email(user.email, code)
                    self.request.session['user_id'] = user.id
                    return redirect('confirmEmail')
                else:
                    form.add_error('email', "This email already exists")
                    return self.form_invalid(form)

            except User.DoesNotExist:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.email = email
                user.is_active = False  # تعطيل الحساب حتى يتم التحقق
                user.save()
                
                code = get_random_string(length=6, allowed_chars='1234567890')
                self.request.session['email_confirmation_code'] = code
                send_confirmation_email(user.email, code)
                self.request.session['user_id'] = user.id
                return redirect('confirmEmail')
        else:
            form.add_error(None, 'الرجاء التحقق من أنك لست روبوت')
            return self.form_invalid(form)

class ConfirmEmailView(View):
    template_name = 'accounts/email_confirm.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'resend' in request.POST:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    code = get_random_string(length=6, allowed_chars='1234567890')
                    request.session['email_confirmation_code'] = code
                    send_confirmation_email(user.email, code)
                    return render(request, self.template_name, {'message': 'OTP resent'})
                except User.DoesNotExist:
                    return render(request, self.template_name, {'error_message': 'User does not exist'})
            else:
                return render(request, self.template_name, {'error_message': 'Session expired, try again.'})
        
        email_confirmation_code = ''.join([
            request.POST.get('otp_digit_1'),
            request.POST.get('otp_digit_2'),
            request.POST.get('otp_digit_3'),
            request.POST.get('otp_digit_4'),
            request.POST.get('otp_digit_5'),
            request.POST.get('otp_digit_6')
        ])
        session_code = request.session.get('email_confirmation_code')
        user_id = request.session.get('user_id')

        if user_id and session_code:
            try:
                user = User.objects.get(id=user_id)
                if session_code == email_confirmation_code:
                    user.is_active = True
                    user.save()
                    login(request, user)
                    del request.session['user_id']
                    del request.session['email_confirmation_code']
                    return redirect('chat')
                else:
                    error_message = 'Invalid confirmation code'
            except User.DoesNotExist:
                error_message = 'User does not exist'
        else:
            error_message = 'Session expired, try again.'
        
        return render(request, self.template_name, {'error_message': error_message})




def login_form(request):
    
    if request.user.is_authenticated:
        return redirect('chat')
    else:
        if request.method == 'POST': 
                email_or_username = request.POST.get('email_or_username')
                password = request.POST.get('password')
                user = authenticate_eu(str(email_or_username), str(password))
                # if recaptcha(request):                      
                if True:
                    if user is not None:
                        login(request, user)

                        try:
                            user = Profile.objects.get(user=request.user.id)
                            return redirect('chat')
                        except Profile.DoesNotExist:
                            return redirect('choose')
                        
                    else:
                        error='User or password is wrong'
                        return render(request, 'accounts/login.html', {'error':error})   

                else:
                    return render(request, 'accounts/login.html', {'error':'الرجاء التحقق  من انك لست روبوت'})

        else:
            return render(request, 'accounts/login.html')

def choose(request):
    try:
        user = Profile.objects.get(user=request.user.id)
        return redirect('chat')
    except Profile.DoesNotExist:
        if request.method == 'POST':
            Profile.objects.create(
                user = request.user,
                name = request.POST.get('name'),
                age = request.POST.get('age'),
                stage = request.POST.get('student_type'),
            ).save
            return redirect('chat')
        age_range = list(range(5, 40))
        return render( request, 'accounts/choose.html', {'age_range':age_range})

def user_logout(request):
    logout(request)
    return redirect('login')


@cache_page(60 * 15)
def TaC(request):
    return render(request, 'accounts/TaC.html')














