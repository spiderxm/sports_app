from django.conf.urls import url, include
from home_app.views import index, sport

app_name = 'home'
urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^sports/$', sport, name="sports")
]
