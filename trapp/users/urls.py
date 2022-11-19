from django.contrib.auth.views import (
    LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    path(
      'logout/',
      LogoutView.as_view(template_name='users/logged_out.html'),
      name='logout'
    ),
    path('signup/', views.SignUp, name='signup'),

    #url('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    views.activate,
    #    name='activate'
    #),
    path(
        'activate/<uidb64>/<token>/',
        views.activate,
        name='activate'
    ),

    #path('signup/done/',
    #     PasswordResetDoneView.as_view(template_name='users/signup_done.html'),
    #     name='signup_done'
    #),

    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(template_name='users/password_reset_form.html'),
        name='password_reset_form'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
]