import re
from django.contrib.auth import authenticate
from django.contrib.auth.models import User



def authenticate_eu(type, password):
    # التحقق إذا كان المدخل بريدًا إلكترونيًا
    def is_email(type):
        pa = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pa, type) is not None

    if is_email(type):
        try:
            user = User.objects.get(email=type)
        except User.DoesNotExist:
            return None
    else:
        try:
      
            user = User.objects.get(username=type)
        except User.DoesNotExist:
            return None

    # التحقق من كلمة المرور باستخدام دالة authenticate
    user = authenticate(username=user.username, password=password)
    if user is not None:
        return user
    else:
        return None
