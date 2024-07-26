from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import update_session_auth_hash
from accounts.tasks import send_confirmation_email
from accounts.models import Profile
from django.contrib import messages
from django.utils.crypto import constant_time_compare
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from openai import OpenAI
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import base64
from django.db.models import F


client = OpenAI(api_key='sk-proj-hT9LIIr6aHF5c7iwCT7LT3BlbkFJH0L1R9TT35yyZ5eKOJiR')

@login_required
@csrf_exempt

def chat(request):
    user = get_object_or_404(Profile, user=request.user.id)
    if user.count > 0:
        if request.method == 'POST':
            if request.POST.get('new_chat') == 'true':
                request.session['chat_history'] = [
                    {"role": "system", "content": "أنت أستاذ لكل المواد الدراسية، ومهمتك هي تعليم الطلاب السودانيين وفقًا للمناهج السودانية."},
                    {"role": "system", "content": "كن مختصرا ولكن ليس لدرجه كبيرة."},
                    {"role": "system", "content": "علم الطالب بالعربي او الانجليزي حسب اللغة التي يتكلمها او يطلبها منك."},
                    {"role": "system", "content": "قدم الشرح بطريقة مبسطة وسهلة الفهم، واستخدم الأمثلة الحية والواقعية التي تتناسب مع البيئة السودانية."},
                    {"role": "system", "content": "اجعل الشرح مشوقًا وجذابًا للطلاب، واستخدم الأساليب التي تحفزهم على التعلم."},
                    {"role": "system", "content": "حافظ على تفاعل إيجابي مع الطلاب وشجعهم على طرح الأسئلة والاستفسارات."},
                    {"role": "system", "content": "استخدم اللغة العربية الفصحى المبسطة في الشرح، وتجنب التعقيدات اللغوية."},
                    {"role": "system", "content": "كن على علم بالمناهج السودانية لكل مادة دراسية، وتأكد من أن الشروح تتوافق مع المناهج المقررة."},
                    {"role": "system", "content": "استخدم أساليب تعليمية مشوقة مثل القصص والألعاب والأمثال المحلية التي تتناسب مع الثقافة السودانية."},
                    {"role": "system", "content": "عند شرح المواد العلمية، استخدم أمثلة وتجارب من الواقع السوداني لتسهيل الفهم."},
                    {"role": "system", "content": "عند شرح المواد الأدبية، استخدم نصوصاً وأمثلة من الأدب السوداني لتعزيز الارتباط بالثقافة المحلية."},
                    {"role": "system", "content": "عند شرح المواد الاجتماعية، استخدم الأمثلة والتطبيقات التي تعكس المجتمع السوداني وتحدياته."},
                    {"role": "system", "content": "عند شرح المواد التاريخية، ركز على التاريخ السوداني والأحداث والشخصيات التاريخية الهامة."}
                ]
                return JsonResponse({'status': 'new chat started'})

            def encode_image(image_file):
                return base64.b64encode(image_file.read()).decode('utf-8')

            user_message = request.POST.get('message')
            chat_history = request.session.get('chat_history', [])

            if 'file' in request.FILES:
                base64_image = encode_image(request.FILES['file'])
                chat_history.append({"role": "user", "content": [
                    {'type': 'text', 'text': user_message},
                    {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{base64_image}"}}
                ]})
            else:
                chat_history.append({"role": "user", "content": [
                    {'type': 'text', 'text': user_message}
                ]})

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=chat_history
            )

            response = completion.choices[0].message.content
            chat_history.append({"role": "assistant", "content": response})
            user.count = F('count') - 1
            user.save()
            request.session['chat_history'] = chat_history

            return JsonResponse({'response': response})
    
            

        else:
            form = ChatForm()
            chat_history = request.session.get('chat_history', [])
            return render(request, 'app/chat.html', {'form': form, 'chat_history': chat_history})
            
    else:
        url = reverse('support') + '?count=0'
        return redirect(url)
#todo.############################ seetings ############################
@login_required
@cache_page(60 * 15)
def setting(request):
    return render(request, 'app/settings.html')

@login_required
@cache_page(60 * 15)
def language(request):
    return render(request, 'app/settings/language.html')

@login_required
@cache_page(60 * 15)
def notifications(request):
    return render(request, 'app/settings/notifications.html')


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('home')
    template_name = 'app/settings/security/change_password.html'
    
    def get_form_kwargs(self):
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.success_url = reverse_lazy("change_password") + "?update=success"
        return super().form_valid(form)
        
    def form_invalid(self, form):
        for error in form.errors:
            print(f"Form is invalid. Errors: {error}")
        return super().form_invalid(form)
 

class Security(LoginRequiredMixin, UpdateView):
    form_class = ChangeEmailUsername
    template_name = 'app/settings/security.html'
    success_url = reverse_lazy("security")

    def get_object(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not request.GET.get('email_change') == 'verification':
            request.session.pop('email_confirmation_code', None)
            request.session.pop('new_email', None)
            request.session.pop('verification_attempts', None)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Security, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if 'new_email' in self.request.session:
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['email'] = self.request.session['new_email']
        return kwargs

    def form_valid(self, form):
        if 'email' in form.changed_data:
            new_email = form.cleaned_data['email']
            # تحقق من صحة البريد الإلكتروني
            try:
                validate_email(new_email)
            except ValidationError:
                form.add_error('email', 'بريد إلكتروني غير صالح.')
                return self.form_invalid(form)

            code = get_random_string(length=6, allowed_chars='1234567890')
            self.request.session['email_confirmation_code'] = code
            self.request.session['new_email'] = new_email
            send_confirmation_email(new_email, code)
            self.success_url = reverse_lazy("security") + "?email_change=verification"
        elif 'username' in form.changed_data:
            self.success_url = reverse_lazy("security") + "?update=success"
            return super().form_valid(form)
        else:
            self.success_url = reverse_lazy("security") + "?update=success"
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        if 'verification_code' in request.POST:
            code = request.POST.get('verification_code')
            session_code = request.session.get('email_confirmation_code')
            verification_attempts = request.session.get('verification_attempts', 0)

            if verification_attempts >= 5:
                self.object = self.get_object()
                context = self.get_context_data(form=self.get_form())
                context['verification_error'] = "تم تجاوز الحد الأقصى لمحاولات التحقق."
                return render(request, self.template_name, context)

            request.session['verification_attempts'] = verification_attempts + 1

            if session_code is None or not constant_time_compare(code, session_code):
                self.object = self.get_object()
                context = self.get_context_data(form=self.get_form())
                context['verification_error'] = "رمز التحقق غير صحيح."
                return render(request, self.template_name, context)

            user = self.get_object()
            user.email = request.session.get('new_email')
            user.save()
            del request.session['email_confirmation_code']
            del request.session['new_email']
            del request.session['verification_attempts']
            self.success_url = reverse_lazy("security") + "?update=success"
            return redirect(self.success_url)

        return super().post(request, *args, **kwargs)


#todo.#################################################################

@login_required
@cache_page(60 * 15)
def support(request):
    return render(request, 'app/support.html')


def payment(request):
    user = Parent.objects.get(id=request.user.id)
    if user.price :
        context = {
            'price' : user.price,
            'son': user.son
        }
        return render(request, 'app/payment.html', context)
    if user.son == 0 and not user.student_name:
        url = reverse('profile') + "?son=0"
        return HttpResponseRedirect(url)

    return redirect('places')
