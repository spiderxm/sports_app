from django.conf.urls import url
from home_app.views import home, sport, news, olympics, add_trial, trial_detail, apply_to_trial

app_name = 'home'
urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^sports/$', sport, name="sports"),
    url(r'^olympics_stats/$', olympics, name="olympic_stats"),
    url(r'^sports_news/$', news, name="news"),
    url(r'^add_trial/$', add_trial, name="add_trial"),
    url(r'^trail/(?P<_id>\d+)/$',trial_detail, name="trial"),
    url(r'^apply_trial/(?P<_id>\d+)/$', apply_to_trial, name="apply_to_trial")

]
