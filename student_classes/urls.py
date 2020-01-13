from django.conf.urls import url

from .views import (scheduled_class_detail_view, scheduled_class_list_view, all_teachers_class_list_view,
                    teacher_class_list_view, teacher_daily_detail_view, attendance_view, past_classes_list_view,
                    all_teachers_daily_detail_view, teacher_past_class_list_view, all_teachers_past_class_list_view)

urlpatterns = [
    url(r'^(?P<id>\d+)/$', scheduled_class_detail_view, name='class-detail'),
    url(r'^student_all/$', scheduled_class_list_view, name='scheduled-classes'),
    url(r'^student_past_all/$', past_classes_list_view, name='past-classes'),
    url(r'^teacher_all/$', teacher_class_list_view, name='teacher-classes'),
    url(r'^teacher_past_classes/$', teacher_past_class_list_view, name='teacher-past-classes'),
    url(r'^teachers_all/$', all_teachers_class_list_view, name='all-teachers-classes'),
    url(r'^teachers_past_classes_all/$', all_teachers_past_class_list_view, name='all-past-teachers-classes'),
    url(r'^(?P<slug>[\w-]+)/teacher_daily/$', teacher_daily_detail_view, name='teacher-daily'),
    url(r'^(?P<slug>[\w-]+)/all_teachers_daily/$', all_teachers_daily_detail_view, name='all-teachers-daily'),
    url(r'^attendance/', attendance_view, name="attendance"),
]