import datetime
import smtplib

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from .models import ContactMessages
from .forms import ContactMessagesForm
from accounts.models import Profile
from class_billing_admin.models import StudentBilling
from student_classes.models import TeacherClass, StudentClass


def message_list_teacher_unconfirmed_view(request):
    query_set = ContactMessages.objects.filter(message_type="teacher_unconfirmed")
    title = 'Messages for Teachers with Unconfirmed Attendance'
    context = {
        'title': title,
        'query_set': query_set,
    }
    template = 'contacts/message_list.html'
    return render(request, template, context)

def message_list_student_unconfirmed_view(request):
    query_set = ContactMessages.objects.filter(message_type="student_unconfirmed")
    title = 'Messages for Students with Unconfirmed Attendance'
    context = {
        'title': title,
        'query_set': query_set,
    }
    template = 'contacts/message_list.html'
    return render(request, template, context)

def message_list_teacher_view(request):
    query_set = ContactMessages.objects.filter(message_type="all_teachers")
    title = 'Messages for Teachers'
    context = {
        'title': title,
        'query_set': query_set,
    }
    template = 'contacts/message_list.html'
    return render(request, template, context)

def message_list_student_view(request):
    query_set = ContactMessages.objects.filter(message_type="all_students")
    title = 'Messages for Students'
    context = {
        'title': title,
        'query_set': query_set,
    }
    template = 'contacts/message_list.html'
    return render(request, template, context)

def message_list_teacher_schedule_view(request):
    query_set = ContactMessages.objects.filter(message_type="teacher_schedules")
    title = 'Scheduling Messages for Teachers'
    context = {
        'title': title,
        'query_set': query_set,
    }
    template = 'contacts/message_list.html'
    return render(request, template, context)

def message_list_student_schedule_view(request):
    query_set = ContactMessages.objects.filter(message_type="student_schedules")
    title = 'Scheduling Messages for Students'
    context = {
        'title': title,
        'query_set': query_set,
    }
    template = 'contacts/message_list.html'
    return render(request, template, context)

def message_list_student_low_hours_view(request):
    query_set = ContactMessages.objects.filter(message_type="students_low_hours")
    title = 'Messages for Students with Low Hours'
    context = {
        'title': title,
        'query_set': query_set,
    }
    template = 'contacts/message_list.html'
    return render(request, template, context)

def message_list_view(request):
    query_set = ContactMessages.objects.filter(message_type="all_users")
    context = {
        'query_set': query_set,
    }
    template = 'contacts/message_list.html'
    return render(request, template, context)

def message_detail_view(request, id=None):
    object = get_object_or_404(ContactMessages, id=id)
    low_student_hours_dict = {}
    if object.message_type == "student_schedules":
        query = StudentClass.custom_query.student_email_query()
    elif object.message_type == "teacher_schedules":
        query = TeacherClass.custom_query.teacher_email_query()
    elif object.message_type == "all_students":
        query = Profile.custom_query.student_email_query()
    elif object.message_type == "all_teachers":
        query = Profile.custom_query.teacher_email_query()
    elif object.message_type == "teacher_unconfirmed":
        qs = StudentClass.custom_query.past_classes_student_confirmed_teacher_unconfirmed()
        query = [scheduled_class.teacherclass.teacher_scheduled for scheduled_class in qs]
    elif object.message_type == "student_unconfirmed":
        qs = StudentClass.custom_query.past_classes_teacher_confirmed_student_unconfirmed()
        profile_query = [scheduled_class.classinformation.students_not_attended() for scheduled_class in qs]
        query = []
        for sub_query in profile_query:
            for q in sub_query:
                if q not in query:
                    query.append(q)
    elif object.message_type == "students_low_hours":
        query = ''
        low_student_hours_dict = StudentBilling.custom_query.student_email_under_two_hours()
    else:
        query = Profile.custom_query.all_users_email_query()
    if request.method == 'POST':
        form = ContactMessagesForm(request.POST or None, instance=object)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
    else:
        form = ContactMessagesForm()
    context = {
        'object': object,
        'low_student_hours_dict': low_student_hours_dict,
        'query': query,
        'form': form,
    }
    if request.is_ajax():
        obj_dict = model_to_dict(object)
        html = render_to_string('contacts/message_form_update.html', context, request=request)
        obj_dict.update({'form': html})
        return JsonResponse(obj_dict)
    template = 'contacts/message_view.html'
    return render(request, template, context)

def teacher_scheduling_email(object, tomorrow, smtpObj, send_from):
    class_query = StudentClass.objects.filter(scheduled_date=tomorrow)
    teacher_email_query = TeacherClass.custom_query.teacher_email_query()
    for teacher in teacher_email_query:
        class_time_list = []
        student_list = []
        for obj in class_query:
            if obj.teacherclass.teacher_scheduled == teacher:
                class_time_list.append(str(obj.scheduled_time)[:5])
                student_list.append(obj.student_scheduled.first().user.username)
        schedule_str = ''
        for c in range(0, len(class_time_list)):
            daily_str = "\r\n%s -- %s" % (class_time_list[c], student_list[c])
            schedule_string = schedule_str
            schedule_str = schedule_string + ' ' + daily_str
        teacher_name = teacher.given_name
        send_to = teacher.contact_email
        message_title = object.title
        message_text = object.message_text
        message_string = '''Subject: %s\n
                            \r\n\r\nHello %s, \r\n\r\nThis is your schedule for tomorrow %s/%s/%s: 
                                %s \r\n\r\n%s \r\n\r\nHave a great day!
                             ''' % (message_title, teacher_name, tomorrow.month, tomorrow.day, tomorrow.year,
                                    schedule_str, message_text)
        smtpObj.sendmail(send_from, send_to, message_string)

def student_scheduling_email(object, tomorrow, smtpObj, send_from):
    class_query = StudentClass.objects.filter(scheduled_date=tomorrow)
    student_email_query = StudentClass.custom_query.student_email_query()
    for student in student_email_query:
        class_time_list = []
        teacher_list = []
        for obj in class_query:
            if student in obj.student_scheduled.all():
                class_time_list.append(str(obj.scheduled_time)[:5])
                teacher_list.append(obj.teacherclass.teacher_scheduled)
                print(obj.teacherclass.teacher_scheduled)
        schedule_str = ''
        for c in range(0, len(class_time_list)):
            daily_str = "\r\n%s -- %s" % (class_time_list[c], teacher_list[c])
            schedule_string = schedule_str
            schedule_str = schedule_string + ' ' + daily_str
        student_name = student.given_name
        send_to = student.contact_email
        message_title = object.title
        message_text = object.message_text
        message_string = '''Subject: %s\n
                            \r\n\r\nHello %s, \r\n\r\nThis is your schedule for tomorrow %s/%s/%s: 
                            %s \r\n\r\n%s \r\n\r\nHave a great day!
                             ''' % (message_title, student_name, tomorrow.month, tomorrow.day, tomorrow.year,
                                    schedule_str, message_text)
        smtpObj.sendmail(send_from, send_to, message_string)

def student_email(object, smtpObj, send_from):
    student_email_query = Profile.custom_query.student_email_query()
    for student in student_email_query:
        student_name = student.given_name
        send_to = student.contact_email
        message_title = object.title
        message_text = object.message_text
        message_string = '''Subject: %s\n
                            \r\n\r\nHello %s, 
                            \r\n\r\n%s \r\n\r\nHave a great day!
                            ''' % (message_title, student_name, message_text)
        smtpObj.sendmail(send_from, send_to, message_string)

def student_low_hours_email(object, smtpObj, send_from):
    account_query = StudentBilling.custom_query.under_two_hours()
    email_list = []
    for account in account_query:
        account_email_list = [account.contact_email for account in account.student_account.all()]
        for email in account_email_list:
            email_list.append(email)
    for email in email_list:
        student_name = 'Valued Customer'
        send_to = email
        message_title = object.title
        message_text = object.message_text
        message_string = '''Subject: %s\n
                            \r\n\r\nDear %s,
                            \r\n%s \r\n\r\nHave a great day!
                            ''' % (message_title, student_name, message_text)
        smtpObj.sendmail(send_from, send_to, message_string)

def teacher_email(object, smtpObj, send_from):
    teacher_email_query = Profile.custom_query.teacher_email_query()
    for teacher in teacher_email_query:
        teacher_name = teacher.given_name
        send_to = teacher.contact_email
        message_title = object.title
        message_text = object.message_text
        message_string = '''Subject: %s\n
                            \r\n\r\nHello %s, 
                            \r\n%s \r\n\r\nHave a great day!
                            ''' % (message_title, teacher_name, message_text)
        smtpObj.sendmail(send_from, send_to, message_string)

def teacher_unconfirmed_attendance_email(object, smtpObj, send_from):
    class_query = StudentClass.custom_query.past_classes_student_confirmed_teacher_unconfirmed()
    for unconfirmed_class in class_query:
        teacher = unconfirmed_class.teacherclass.teacher_scheduled
        class_time = unconfirmed_class.scheduled_time
        class_date = unconfirmed_class.scheduled_date
        student_list = unconfirmed_class.students_scheduled()
        info_str = ','.join(map(str, student_list))
        teacher_name = teacher.given_name
        send_to = teacher.contact_email
        message_title = object.title
        message_text = object.message_text
        message_string = '''Subject: %s\n
                            \r\n\r\nHello %s, \r\n\r\nPlease confirm attendance for the class on %s at %s with the students: 
                            \r\n%s \r\n\r\n%s \r\n\r\nHave a great day!
                             ''' % (message_title, teacher_name, class_date, class_time,
                                    info_str, message_text)
        smtpObj.sendmail(send_from, send_to, message_string)

def student_unconfirmed_attendance_email(object, smtpObj, send_from):
    class_query = StudentClass.custom_query.past_classes_teacher_confirmed_student_unconfirmed()
    for unconfirmed_class in class_query:
        teacher = unconfirmed_class.teacherclass.teacher_scheduled
        class_time = unconfirmed_class.scheduled_time
        class_date = unconfirmed_class.scheduled_date
        student_list = unconfirmed_class.students_scheduled()
        for student in student_list:
            student_name = student.given_name
            send_to = student.contact_email
            message_title = object.title
            message_text = object.message_text
            message_string = '''Subject: %s\n
                                        \r\n\r\nHello %s, \r\n\r\nPlease confirm attendance for the class on %s at %s with the teacher: 
                                        \r\n%s \r\n\r\n%s \r\n\r\nHave a great day!
                                         ''' % (message_title, student_name, class_date, class_time,
                                                teacher, message_text)
            smtpObj.sendmail(send_from, send_to, message_string)

def general_email(object, smtpObj, send_from):
    user_email_query = Profile.custom_query.all_users_email_query()
    for user in user_email_query:
        user_name = user.given_name
        send_to = user.contact_email
        message_title = object.title
        message_text = object.message_text
        message_string = '''Subject: %s\n
                            \r\n\r\nHello %s, 
                            \r\n%s \r\n\r\nHave a great day!
                            ''' % (message_title, user_name, message_text)
        smtpObj.sendmail(send_from, send_to, message_string)

def message_sent_view(request, id=None):
    low_student_hours_dict = {}
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    object = get_object_or_404(ContactMessages, id=id)
    send_from = object.email
    pwd = object.pwd
    smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(send_from, pwd)
    if object.message_type == "teacher_schedules":
        email_query = TeacherClass.custom_query.teacher_email_query()
        teacher_scheduling_email(object, tomorrow, smtpObj, send_from)
        smtpObj.quit()
    elif object.message_type == "student_schedules":
        email_query = StudentClass.custom_query.student_email_query()
        student_scheduling_email(object, tomorrow, smtpObj, send_from)
        smtpObj.quit()
    elif object.message_type == "all_teachers":
        email_query = Profile.custom_query.teacher_email_query()
        teacher_email(object, smtpObj, send_from)
        smtpObj.quit()
    elif object.message_type == "all_students":
        email_query = Profile.custom_query.student_email_query()
        student_email(object, smtpObj, send_from)
        smtpObj.quit()
    elif object.message_type == "students_low_hours":
        email_query = ''
        low_student_hours_dict = StudentBilling.custom_query.student_email_under_two_hours()
        student_low_hours_email(object, smtpObj, send_from)
        smtpObj.quit()
    elif object.message_type == 'teacher_unconfirmed':
        qs = StudentClass.custom_query.past_classes_student_confirmed_teacher_unconfirmed()
        email_query = [scheduled_class.teacherclass.teacher_scheduled for scheduled_class in qs]
        teacher_unconfirmed_attendance_email(object, smtpObj, send_from)
        smtpObj.quit()
    elif object.message_type == 'student_unconfirmed':
        qs = StudentClass.custom_query.past_classes_teacher_confirmed_student_unconfirmed()
        profile_query = [scheduled_class.classinformation.students_not_attended() for scheduled_class in qs]
        email_query = []
        for sub_query in profile_query:
            for q in sub_query:
                if q not in email_query:
                    email_query.append(q)
        student_unconfirmed_attendance_email(object, smtpObj, send_from)
        smtpObj.quit()
    else:
        email_query = Profile.custom_query.all_users_email_query()
        general_email(object, smtpObj, send_from)
        smtpObj.quit()
    obj = object
    obj.pwd = ''
    obj.save()
    context = {
        'object': object,
        'low_student_hours_dict': low_student_hours_dict,
        'user_query': email_query,
    }
    template = 'contacts/message_sent.html'
    return render(request, template, context)