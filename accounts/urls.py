from django.conf.urls import url

from .views import register, user_login, user_logout, profile_model_detail_view, student_profile_detail_view

urlpatterns = [
    url(r'^profile/$', profile_model_detail_view, name='profile-detail'), #user regular expression for username
    url(r'^(?P<id>\d+)/$', student_profile_detail_view, name='student-detail'),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
]