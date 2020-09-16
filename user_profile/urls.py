from django.conf.urls import url
from user_profile.views import profile, upload_photo, add_achievement, add_certificate

urlpatterns = [
    url(r'^(?P<_id>\d+)/$', profile, name="user_profile"),
    url(r'^upload_photo/(?P<_id>\d+)/$', upload_photo, name="upload_photo"),
    url(r'^add_achievement/(?P<_id>\d+)/$', add_achievement, name="add_achievement"),
    url(r'^add_acertificate/(?P<_id>\d+)/$', add_certificate, name="add_certificate")

]
