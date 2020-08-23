from django.conf.urls import url
from verification import views

urlpatterns = [
    url('login/', views.login, name="login"),
    url('register/', views.register, name="register"),
    url('logout/', views.Logout,name="logout")
]
