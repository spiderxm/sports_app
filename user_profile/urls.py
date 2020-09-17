from django.conf.urls import url
from user_profile.views import profile, upload_photo, add_achievement, add_certificate, view_trial_application_details

urlpatterns = [
    url(r'^(?P<_id>\d+)/$', profile, name="user_profile"),
    url(r'^upload_photo/$', upload_photo, name="upload_photo"),
    url(r'^add_achievement/$', add_achievement, name="add_achievement"),
    url(r'^add_certificate/$', add_certificate, name="add_certificate"),
    url(r'^trial_application_info/(?P<_id>\d+)/$', view_trial_application_details, name="trial_application_info")
]
