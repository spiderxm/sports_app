from django.conf.urls import url
from home_app.views import index, sport, news, olympics, add_trial

app_name = 'home'
urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^sports/$', sport, name="sports"),
    url(r'^olympics_stats/$', olympics, name="olympic_stats"),
    url(r'^sports_news/$', news, name="news"),
    url(r'^add_trial/$', add_trial, name="add_trial")

]
