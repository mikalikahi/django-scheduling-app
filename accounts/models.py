from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

class ProfileManager(models.Manager):
    def student_email_query(self):
        student_email_query = []
        for student in self.get_queryset():
            if student.student == True and student not in student_email_query:
                student_email_query.append(student)
        return student_email_query

    def teacher_email_query(self):
        teacher_email_query = []
        for teacher in self.get_queryset():
            if teacher.teacher == True and teacher not in teacher_email_query:
                teacher_email_query.append(teacher)
        return teacher_email_query

    def all_users_email_query(self):
        all_users_email_query = []
        for user in self.get_queryset():
            if user not in all_users_email_query:
                all_users_email_query.append(user)
        return all_users_email_query


class Profile(models.Model):
    custom_query = ProfileManager()
    objects = models.Manager()
    #classes_purchased =
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    contact_email = models.EmailField(max_length=200, null=True, blank=True)
    surname = models.CharField(max_length=120, null=True, blank=True)
    given_name = models.CharField(max_length=120, null=True, blank=True)
    teacher = models.BooleanField(default=False)
    student = models.BooleanField(default=False)
    course_content_preferences = models.TextField(editable=True, default='', blank=True)
    other_personal_information = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.user.username

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass
post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
