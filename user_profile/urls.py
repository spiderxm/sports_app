from django.conf.urls import url
from user_profile.views import profile, upload_photo

urlpatterns = [
    url(r'^(?P<_id>\d+)/$', profile, name="user_profile"),
    url(r'^upload_photo/(?P<_id>\d+)/$', upload_photo, name="upload_photo")
]
