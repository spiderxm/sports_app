from django.conf.urls import url
from verification import views
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

urlpatterns = [
    url('login/', views.login, name="login"),
    url('register/', views.register, name="register"),
    url('logout/', views.Logout, name="logout"),
    url(r'^password-reset/$', PasswordResetView.as_view(template_name="verification/password_reset.html"),
        name="password_reset"),
    url(r'^password-reset-done/$', PasswordResetDoneView.as_view(template_name="verification/password_reset_done.html"),
        name="password_reset_done"),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name="verification/password_reset_confirm.html"),
        name="password_reset_confirm"),
]
