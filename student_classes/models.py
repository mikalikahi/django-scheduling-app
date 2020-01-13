import datetime

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.template.defaultfilters import slugify

from accounts.models import Profile
from class_locations.models import ClassLocation
from class_billing_admin.models import StudentBilling
from teacher_billing.models import TeacherCustomBillingRates, TeacherBillingPeriod

def schedule_date_list(list_of_classes):
    return list_of_classes.scheduled_date

class StudentClassManager(models.Manager):
    def student_email_query(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        student_email_query = []
        for scheduled_class in self.get_queryset():
            if scheduled_class.scheduled_date == tomorrow:
                student_list = scheduled_class.student_scheduled.all()
                for student in student_list:
                    if student not in student_email_query:
                        student_email_query.append(student)
        return student_email_query

    def past_classes(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        past_classes = [scheduled_class for scheduled_class in self.get_queryset() if scheduled_class.scheduled_date <= yesterday]
        past_classes.sort(key=schedule_date_list, reverse=True)
        return past_classes

    def past_classes_teacher_confirmed_attendance(self):
        teacher_attended = [scheduled_class for scheduled_class in self.past_classes() if scheduled_class.classinformation.teacher_attended == True]
        return teacher_attended

    def past_classes_student_confirmed_attendance(self):
        student_attended = [scheduled_class for scheduled_class in self.past_classes() \
                            if scheduled_class.classinformation.students_in_attendance.all().count() >= 1]
        return student_attended

    def past_classes_teacher_confirmed_student_unconfirmed(self):
        teacher_attended_student_unconfirmed = [scheduled_class for scheduled_class in self.past_classes_teacher_confirmed_attendance() \
                                                if scheduled_class not in self.past_classes_student_confirmed_attendance()]
        return teacher_attended_student_unconfirmed

    def past_classes_student_confirmed_teacher_unconfirmed(self):
        student_attended_teacher_unconfirmed = [scheduled_class for scheduled_class in self.past_classes_student_confirmed_attendance() \
                                                if scheduled_class not in self.past_classes_teacher_confirmed_attendance()]
        return student_attended_teacher_unconfirmed

    def upcoming_classes(self):
        upcoming_classes = [scheduled_class for scheduled_class in self.get_queryset() if scheduled_class.scheduled_date >= datetime.date.today()]
        upcoming_classes.sort(key=schedule_date_list)
        return upcoming_classes

class StudentClass(models.Model):
    custom_query = StudentClassManager()
    objects = models.Manager()
    student_scheduled = models.ManyToManyField(Profile, limit_choices_to={'student': True}, related_name='student_scheduled')
    scheduled_date = models.DateField(blank=True, null=True)
    scheduled_time = models.TimeField(blank=True, null=True)
    schedule_time_finish = models.TimeField(blank=True, null=True)
    slug = models.SlugField(max_length=50, blank=True, null=True)

    def students_scheduled(self):
        return self.student_scheduled.all()

    def students_scheduled_list(self):
        students = [obj for obj in self.students_scheduled()]
        return students

    def date_time_booked(self):
        booked = StudentClass.objects.filter(Q(scheduled_date=self.scheduled_date)) \
                                        .filter(Q(scheduled_time__gte=self.scheduled_time)  &
                                                Q(scheduled_time__lte=self.schedule_time_finish) |
                                                Q(schedule_time_finish__gte=self.scheduled_time) &
                                                Q(schedule_time_finish__lte=self.schedule_time_finish))
        return booked

    def unavailable_teachers(self):
        qs_date_time = self.date_time_booked()
        teacher_qs = []
        for t in qs_date_time:
            if t.teacherclass.teacher_scheduled not in teacher_qs and t.teacherclass.teacher_scheduled != None:
                teacher_qs.append(t.teacherclass.teacher_scheduled)
        return teacher_qs

    def unavailable_classroom(self):
        qs_date_time = self.date_time_booked()
        classroom_qs = []
        for c in qs_date_time:
            if c.classinformation.location not in classroom_qs and c.classinformation.location != None and \
                                                c.classinformation.location.location_name == 'TLI_Roosevelt':
                classroom_qs.append(c.classinformation.location)
        return classroom_qs

    def __str__(self):
        student = self.students_scheduled()
        return "{} on {} at {}".format(student[0], self.scheduled_date, self.scheduled_time)

    class Meta:
        verbose_name_plural = 'Student Classes'

class TeacherClassManager(models.Manager):
    def teacher_email_query(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        teacher_email_query = []
        for scheduled_class in self.get_queryset():
            if scheduled_class.student_class.scheduled_date == tomorrow and scheduled_class.teacher_scheduled not in teacher_email_query:
                teacher_email_query.append(scheduled_class.teacher_scheduled)
        return teacher_email_query

class TeacherClass(models.Model):
    objects = models.Manager()
    custom_query = TeacherClassManager()
    student_class = models.OneToOneField(StudentClass, on_delete=models.CASCADE, primary_key=True)
    teacher_scheduled = models.ForeignKey(Profile, limit_choices_to={'teacher': True}, null=True, blank=True,
                                          related_name='teacher_scheduled')
    hours_billed = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    custom_billing = models.ForeignKey(TeacherCustomBillingRates, null=True, blank=True)

    def get_billing_information(self):
        information_dict = {
            'billing_account': '',
            'billing_period': '',
            'billing_type': '',
            'billed_hours': self.hours_billed
        }
        billing_period = [period.id for period in TeacherBillingPeriod.objects.all() \
                           if self.student_class.scheduled_date >= period.start_date \
                           and self.student_class.scheduled_date <= period.finish_date]
        information_dict['billing_period'] = billing_period
        information_dict['billing_account'] = self.student_class.classinformation.student_billing_account
        if self.custom_billing:
            if self.custom_billing.teacher_billed:
                information_dict['billing_type'] = 'custom_for_teacher'
            else:
                information_dict['billing_type'] = 'customized_nonspecified_teacher'
        else:
            if self.student_class.classinformation.location \
                    and self.student_class.classinformation.location.location_name == 'TLI_Roosevelt':
                information_dict['billing_type'] = 'inside'
            else:
                information_dict['billing_type'] = 'outside'
        return information_dict

    def __str__(self):
        return "{} on {} at {}".format(self.teacher_scheduled, self.student_class.scheduled_date,
                                       self.student_class.scheduled_time)

    class Meta:
        verbose_name_plural = 'Teacher Classes'

CLASS_STATUS = (
    ('scheduled', 'Scheduled'),
    ('cancellation_request', 'Cancellation_Request'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
    ('same_day_cancellation', 'Same_Day_Cancellation'),
    )

class ClassInformation(models.Model):
    student_class = models.OneToOneField(StudentClass, on_delete=models.CASCADE, primary_key=True)
    location = models.ForeignKey(ClassLocation, blank=True, null=True)
    class_status = models.CharField(max_length=300, choices=CLASS_STATUS, default='scheduled')
    teacher_attended = models.BooleanField(default=False)
    students_in_attendance = models.ManyToManyField(User, related_name='students_in_attendance', blank=True)
    student_attended = models.BooleanField(default=False)
    class_content = models.TextField(editable=True, default='', blank=True)
    absence_request_reason = models.TextField(editable=True, default='', blank=True)
    student_billing_account = models.ForeignKey(StudentBilling, null=True, blank=True)

    def get_billing_type(self): # this is unnecessary
        if self.student_billing_account in TeacherCustomBillingRates.custom_query.get_customized_accounts():
            billing_type = 'specialized'
        else:
            if self.location and self.location.location_name == 'TLI_Roosevelt':
                billing_type = 'inside'
            else:
                billing_type = 'outside'
        return billing_type

    def students_who_attended(self):
        return self.students_in_attendance.all()

    def students_not_attended(self):
        scheduled = [student for student in self.student_class.students_scheduled() if student not in self.students_who_attended()]
        return scheduled

    def __str__(self):
        student_list = [student.user.username for student in self.student_class.students_scheduled()]
        student_list_str = ", ".join(student_list )
        return "Class info for {} on {} at {} with {} at {}".format(student_list_str,
                                                        self.student_class.scheduled_date,
                                                        self.student_class.scheduled_time,
                                                        self.student_class.teacherclass.teacher_scheduled,
                                                        self.location)

    class Meta:
        verbose_name_plural = 'Class Information'

@receiver(pre_save, sender=StudentClass)
def pre_save_slug(sender, **kwargs):
    #print(kwargs) #try this to find the keyword arguments used below ie 'instance'
    slug = slugify(kwargs['instance'].scheduled_date)
    kwargs['instance'].slug = slug

def post_save_teacher_class_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            TeacherClass.objects.create(student_class=instance)
        except:
            pass
post_save.connect(post_save_teacher_class_receiver, sender=StudentClass)

def post_save_class_information_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            ClassInformation.objects.create(student_class=instance)
        except:
            pass
post_save.connect(post_save_class_information_receiver, sender=StudentClass)