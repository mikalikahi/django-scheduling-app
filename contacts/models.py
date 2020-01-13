from django.db import models

MESSAGE_TYPE = (
    ("teacher_unconfirmed", "Teacher Attendance Unconfirmed"),
    ("student_unconfirmed", "Student Attendance Unconfirmed"),
    ("teacher_schedules", "Teacher's Schedules"),
    ("student_schedules", "Student's Schedules"),
    ("all_teachers", "All Teachers"),
    ("all_students", "All Students"),
    ("students_low_hours", "Students Low on Hours"),
    ("all_users", "All Users"),
    )

class ContactMessages(models.Model):
    title = models.CharField(max_length=120)
    message_text = models.TextField()
    message_type = models.CharField(max_length=300, choices=MESSAGE_TYPE, default='teacher_schedules')
    timestamp = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    pwd = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Contact Messages'
