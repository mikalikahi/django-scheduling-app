from django.conf.urls import url

from .views import message_list_view, message_detail_view, message_sent_view, message_list_student_schedule_view, \
                    message_list_teacher_view, message_list_student_view, message_list_teacher_schedule_view, \
                    message_list_student_low_hours_view, message_list_student_unconfirmed_view, \
                    message_list_teacher_unconfirmed_view

urlpatterns = [
    url(r'^message_list_teacher_unconfirmed/$', message_list_teacher_unconfirmed_view, name="message_list_teacher_unconfirmed"),
    url(r'^message_list_student_unconfirmed/$', message_list_student_unconfirmed_view, name="message_list_student_unconfirmed"),
    url(r'^message_list_teacher/$', message_list_teacher_view, name="message_list_teacher"),
    url(r'^message_list_student/$', message_list_student_view, name="message_list_student"),
    url(r'^message_list_student_low_hours/$', message_list_student_low_hours_view, name="message_list_student_low_hours"),
    url(r'^message_list_teacher_schedule/$', message_list_teacher_schedule_view, name="message_list_teacher_schedule"),
    url(r'^message_list_student_schedule/$', message_list_student_schedule_view, name="message_list_student_schedule"),
    url(r'^message_list/$', message_list_view, name="message_list"),
    url(r'^(?P<id>\d+)/message_sent/$', message_sent_view, name="message_sent"),
    url(r'^(?P<id>\d+)/$', message_detail_view, name="message_detail"),
]