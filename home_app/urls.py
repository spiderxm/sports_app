from django.conf.urls import url
from home_app.views import index, sport, news, olympics

app_name = 'home'
urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^sports/$', sport, name="sports"),
    url(r'^olympics_stats/$', olympics, name="olympic_stats"),
    url(r'^sports_news/$', news, name="news")

]
