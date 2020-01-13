from django.conf.urls import url

from .views import schedule_daily_detail_view, schedule_list_view

urlpatterns = [
    url(r'^(?P<id>\d+)/$', schedule_daily_detail_view, name='daily-detail'),
    url(r'^all/$', schedule_list_view, name='scheduled-dates'),
]