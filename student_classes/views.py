import datetime

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict

from .models import StudentClass, TeacherClass, ClassInformation
from .forms import UpdateTeacherAttendance, UpdateStudentAttendance, UpdateClassStatus
from accounts.models import Profile
from class_billing_admin.models import StudentBilling
from teacher_billing.models import (TeacherBillingHours, TeacherCustomBillingHours,
                                    TeacherBillingPeriod, TeacherCumulativeCustomBillingHours,
                                    TeacherCumulativeMonthlyPayment, TeacherTotalBillingHours,
                                    TeacherTotalCustomBillingHours)

User = get_user_model()
profile = Profile

def save_billing_information(billing_information, teacher, billing_pk, object):
    print('The obj is this type of class: {}'.format(billing_information['billing_type']))
    if billing_information['billing_type'] == 'custom_for_teacher' or \
            billing_information['billing_type'] == 'customized_nonspecified_teacher':
        billing_obj = TeacherCustomBillingHours.objects.get_or_create(teacher_billed=teacher, \
                                                                            billing=TeacherBillingPeriod.objects.filter(
                                                                            pk=billing_pk).first(), \
                                                                            account=object.student_billing_account)[0]
        if billing_obj.billed_hours == None:
            billing_obj.billed_hours = billing_information['billed_hours']
        else:
            billing_obj.billed_hours = billing_obj.billed_hours + billing_information['billed_hours']
        billing_obj.save()
    elif billing_information['billing_type'] == 'inside':
        billing_obj_tuple = TeacherBillingHours.objects.get_or_create(billing=TeacherBillingPeriod.objects.filter(pk=billing_pk).first(), \
                                                                      teacher_billed=teacher)
        billing_obj = billing_obj_tuple[0]
        if billing_obj.billed_hours == None:
            billing_obj.billed_hours = billing_information['billed_hours']
        else:
            billing_obj.billed_hours = billing_obj.billed_hours + billing_information['billed_hours']
            print('This is the amount of billed hours: {}'.format(billing_obj.billed_hours))
        billing_obj.save()
        print('This is the amount of billed hours: {}'.format(billing_obj.billed_hours))
    else:
        billing_obj_tuple = TeacherBillingHours.objects.get_or_create(billing=TeacherBillingPeriod.objects.filter(pk=billing_pk).first(), \
                                                                      teacher_billed=teacher)
        billing_obj = billing_obj_tuple[0]
        if billing_obj.outside_billed_hours == None:
            billing_obj.outside_billed_hours = billing_information['billed_hours']
        else:
            billing_obj.outside_billed_hours = billing_obj.outside_billed_hours + billing_information['billed_hours']
        billing_obj.save()
        print('This is the amount of billed hours: {}'.format(billing_obj.billed_hours))

def scheduled_class_detail_view(request, id=None):
    current_user = request.user
    obj = StudentClass.objects.get(id=id)
    object = obj.classinformation
    class_is_upcoming = True
    today_date = datetime.datetime.now()
    if obj.scheduled_date <= datetime.datetime.date(today_date):
        class_is_upcoming = False
    original_teacher_attendance = object.teacher_attended
    form = None
    is_teacher_attendance_form = False
    if current_user.profile.teacher == True:
        form = UpdateTeacherAttendance(request.POST or None, instance=object)
        is_teacher_attendance_form = True
    else:
        form = UpdateClassStatus(request.POST or None, instance=object)
    attended = False
    if object.students_in_attendance.filter(id=request.user.id).exists():
        attended = True
    context = {
        "obj": obj,
        "object": object,
        "class_is_upcoming": class_is_upcoming,
        "current_user": current_user,
        "attended": attended,
        "form": form,
    }
    if form.is_valid():
        obj_dict = model_to_dict(obj)
        object_dict = model_to_dict(object)
        object_dict.update(obj_dict)
        if is_teacher_attendance_form == True and object_dict['teacher_attended'] == True and original_teacher_attendance == False:
            billing_information = obj.teacherclass.get_billing_information()
            print('This is the account: {}'.format(billing_information['billing_account']))
            teacher = obj.teacherclass.teacher_scheduled
            billing_pk = billing_information['billing_period'][0]
            print(billing_information['billing_type'])
            save_billing_information(billing_information, teacher, billing_pk, object)
            #save_cumulative_monthly_payment(teacher, billing_pk)
        if is_teacher_attendance_form == True and object_dict['teacher_attended'] == False and original_teacher_attendance == True:
            billing_information = obj.teacherclass.get_billing_information()
            teacher = obj.teacherclass.teacher_scheduled
            print(billing_information['billing_type'])
            amount_of_billed_hours = billing_information['billed_hours']
            print('This many hours are billed {}'.format(amount_of_billed_hours))
            billing_information['billed_hours'] = -billing_information['billed_hours']
            print('This many hours should be subtracted {}'.format(billing_information['billed_hours']))
            billing_pk = billing_information['billing_period'][0]
            save_billing_information(billing_information, teacher, billing_pk, object)
            #save_cumulative_monthly_payment(teacher, billing_pk)
        info_obj = form.save(commit=False)
        info_obj.save()
        messages.success(request, "You have updated class information!")
    template = "student_classes/scheduled-class-detail-view.html"
    return render(request, template, context)

def attendance_view(request):
    #object = get_object_or_404(ClassInformation, id=request.POST.get('object_id'))
    object = get_object_or_404(ClassInformation, pk=request.POST.get('id'))
    attended = False
    if object.students_in_attendance.filter(id=request.user.id).exists():
        object.students_in_attendance.remove(request.user)
        attended = False
        if object.students_who_attended().count() == 0:
            account_id = object.student_billing_account.id
            account_obj = StudentBilling.objects.get(id=account_id)
            account_obj.purchased_class_hours += 1
            account_obj.save()
    else:
        object.students_in_attendance.add(request.user)
        attended = True
        if object.students_who_attended().count() == 1:
            account_id = object.student_billing_account.id
            account_obj = StudentBilling.objects.get(id=account_id)
            account_obj.purchased_class_hours -= 1
            account_obj.save()
    context = {
        "object": object,
        "attended": attended,
    }
    if request.is_ajax():
        html = render_to_string('student_classes/attendance_section.html', context, request=request)
        return JsonResponse({'form': html})

def scheduled_class_list_view(request):
    current_user = request.user
    current_student_profile = Profile.objects.get(user=current_user)
    current_student_schedule = []
    schedule_list = StudentClass.custom_query.upcoming_classes()
    for scheduled_date in schedule_list:
        if current_student_profile in scheduled_date.students_scheduled():
            current_student_schedule.append(scheduled_date)
    context = {
        'heading': "Upcoming Classes",
        'student_schedule_query': current_student_schedule,
        'user_student': current_user,
    }
    template = "student_classes/scheduled-class-list-view.html"
    return render(request, template, context)

def past_classes_list_view(request):
    current_user = request.user
    current_student_profile = Profile.objects.get(user=current_user)
    current_student_schedule = []
    schedule_list = StudentClass.custom_query.past_classes()
    for scheduled_date in schedule_list:
        if current_student_profile in scheduled_date.students_scheduled():
            current_student_schedule.append(scheduled_date)
    context = {
        'heading': "Past Classes",
        'student_schedule_query': current_student_schedule,
        'user_student': current_user,
    }
    template = "student_classes/scheduled-class-list-view.html"
    return render(request, template, context)

def teacher_class_list_view(request):
    current_user = request.user
    current_teacher_profile = Profile.objects.get(user=current_user)
    current_teacher_schedule = []
    list_of_class_dates = []
    schedule_list = StudentClass.custom_query.upcoming_classes()
    for scheduled_class in schedule_list:
        if scheduled_class.teacherclass.teacher_scheduled == current_teacher_profile and scheduled_class.scheduled_date not in list_of_class_dates:
            current_teacher_schedule.append(scheduled_class)
            list_of_class_dates.append(scheduled_class.scheduled_date)
    context = {
        'heading': "Scheduled Classes",
        'teacher_schedule_query': current_teacher_schedule,
        'user_teacher': current_user,
    }
    template = "student_classes/teacher-class-list-view.html"
    return render(request, template, context)

def teacher_past_class_list_view(request):
    current_user = request.user
    current_teacher_profile = Profile.objects.get(user=current_user)
    current_teacher_schedule = []
    list_of_class_dates = []
    schedule_list = StudentClass.custom_query.past_classes()
    for scheduled_class in schedule_list:
        if scheduled_class.teacherclass.teacher_scheduled == current_teacher_profile and scheduled_class.scheduled_date not in list_of_class_dates:
            current_teacher_schedule.append(scheduled_class)
            list_of_class_dates.append(scheduled_class.scheduled_date)
    context = {
        'heading': "Past Classes",
        'teacher_schedule_query': current_teacher_schedule,
        'user_teacher': current_user,
    }
    template = "student_classes/teacher-class-list-view.html"
    return render(request, template, context)

def teacher_daily_detail_view(request, slug=None):
    current_user = request.user
    teacherclass_query = TeacherClass.objects.filter(teacher_scheduled=current_user.profile).first()
    current_teacher = teacherclass_query.teacher_scheduled
    class_slug_query = StudentClass.objects.filter(slug=slug)
    qs = []
    for obj in class_slug_query:
        if obj.teacherclass.teacher_scheduled == current_teacher:
            qs.append(obj)
 #   obj = get_object_or_404(PostModel, id=id)
    context = {
        "user_query": qs,
        "scheduled_date": slug,
        "user": current_user,
    }
    template = "student_classes/teacher-daily-detail-view.html"
    return render(request, template, context)

def all_teachers_class_list_view(request):
    teacher_schedule = []
    list_of_class_dates = []
    schedule_list = StudentClass.custom_query.upcoming_classes()
    for scheduled_class in schedule_list:
        if scheduled_class.scheduled_date not in list_of_class_dates:
            teacher_schedule.append(scheduled_class)
            list_of_class_dates.append(scheduled_class.scheduled_date)
    context = {
        'teacher_schedule_query': teacher_schedule,
    }
    template = "student_classes/all-teachers-class-list-view.html"
    return render(request, template, context)

def all_teachers_past_class_list_view(request):
    teacher_schedule = []
    list_of_class_dates = []
    schedule_list = StudentClass.custom_query.past_classes()
    for scheduled_class in schedule_list:
        if scheduled_class.scheduled_date not in list_of_class_dates:
            teacher_schedule.append(scheduled_class)
            list_of_class_dates.append(scheduled_class.scheduled_date)
    context = {
        'teacher_schedule_query': teacher_schedule,
    }
    template = "student_classes/all-teachers-class-list-view.html"
    return render(request, template, context)

def all_teachers_daily_detail_view(request, slug=None):
    class_slug_query = StudentClass.objects.filter(slug=slug)
    teacher_qs = []
    for obj in class_slug_query:
        if obj.teacherclass.teacher_scheduled not in teacher_qs:
            teacher_qs.append(obj.teacherclass.teacher_scheduled)
    context = {
        "scheduled_class_query": class_slug_query,
        "teacher_query": teacher_qs,
        "scheduled_date": slug,
    }
    template = "student_classes/all-teachers-daily-detail-view.html"
    return render(request, template, context)