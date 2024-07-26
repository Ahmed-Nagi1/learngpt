from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('support/', views.support, name='support'),
    path('payment/', views.payment, name='payment'),
    path('settings/', views.setting, name='settings'),
    path('security/language/', views.language, name='language'),
    path('security/', views.Security.as_view(), name='security'),
    path('security/notifications/', views.notifications, name='notifications'),
    path('security/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)