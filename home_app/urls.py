from django.conf.urls import url
from django.conf.urls.static import static
from home_app.views import home, sport, news, olympics, add_trial, trial_detail, apply_to_trial, trial, users_list
from django.conf import settings

app_name = 'home'
urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^sports/$', sport, name="sports"),
    url(r'^olympics_stats/$', olympics, name="olympic_stats"),
    url(r'^sports_news/$', news, name="news"),
    url(r'^add_trial/$', add_trial, name="add_trial"),
    url(r'^trial/(?P<_id>\d+)/$', trial_detail, name="trial"),
    url(r'^trials/$', trial, name="trials"),
    url(r'^users/$', users_list, name="users"),
    url(r'^apply_trial/(?P<_id>\d+)/$', apply_to_trial, name="apply_to_trial"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
