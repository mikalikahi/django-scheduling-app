from django.shortcuts import render#, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

from accounts.models import Profile
from student_classes.models import TeacherClass, StudentClass

# Create your views here.

def schedule_daily_detail_view(request, id=None):
    current_user = request.user
    obj = TeacherClass.objects.get(id=id)
    print(obj)
 #   obj = get_object_or_404(PostModel, id=id)
    context = {
        "object": obj,
        "user": current_user,
    }
    template = "schedule/daily-detail-view.html"
    return render(request, template, context)

def schedule_list_view(request):
    current_user = request.user
    current_user_profile = Profile.objects.get(user=current_user)
    #   obj = get_object_or_404(Profile, id=id) or maybe ClassSchedule or maybe ClassSchedule
    current_user_schedule = []
    schedule_list = ClassSchedule.objects.all().order_by('scheduled_date')
    for schedule_date in schedule_list:
        if schedule_date.profile == current_user_profile:
            current_user_schedule.append(schedule_date)

    context = {
        'schedule_query': current_user_schedule,
        'user': current_user,
    }
    template = "schedule/schedule-list-view.html"
    return render(request, template, context)

