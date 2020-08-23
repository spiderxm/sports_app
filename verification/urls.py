from django.conf.urls import url
from verification import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('login/', views.login, name="login"),
    url('register/', views.register, name="register"),
    # url('home/')

]
