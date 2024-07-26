from django.contrib.auth import views as authViews
from django.urls import path
from . import views

urlpatterns= [
    path('', views.redirect_login),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.login_form, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('reset_password/', authViews.PasswordResetView.as_view(template_name='accounts/reset_password.html'), name= 'password_reset'),
    path('reset_password_sent/', authViews.PasswordResetDoneView.as_view(template_name='accounts/reset_password_sent.html'), name= 'password_reset_done'),
    path('reset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'), name= 'password_reset_confirm'),
    path('reset_password_complete/', authViews.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'), name= 'password_reset_complete'),

    path('confirm_email/', views.ConfirmEmailView.as_view(), name='confirmEmail'),

    path('choose/', views.choose, name='choose'),
    path('TaC/', views.TaC, name='TaC'),
    




]

