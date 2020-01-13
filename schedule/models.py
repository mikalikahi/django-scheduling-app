from django.db import models
from django.conf import settings

# Create your models here.
#User = settings.AUTH_USER_MODEL

#from accounts.models import Profile # try limit_choices_to User id's for people who are teachers
                                    # do this using a filter function off profiles

# Create your models here.
#class ClassSchedule(models.Model):
#    profile = models.ForeignKey(Profile, limit_choices_to={'teacher': True}, null=True, related_name='teacher_schedule')
#    work_date = models.DateField(auto_now=False) #DateField #unique=True
#    seven_thirty_eight_twenty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_one')
#    eight_thirty_nine_twenty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_two')
#    nine_thirty_ten_twenty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_three')
#    ten_thirty_eleven_twenty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_four')
#    elevent_thirty_twelve_twenty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_five')
#    twelve_forty_thirteen_thirty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_six')
#    thirteen_forty_fourteen_thirty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_seven')
#    fourteen_forty_fifteen_thirty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_eight')
#    fifteen_forty_sixteen_thirty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_nine')
#    sixteen_forty_seventeen_thirty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_ten')
#    seventeen_forty_eighteen_thirty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_eleven')
#    eighteen_forty_nineteen_thirty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_twelve')
#    nineteen_forty_twenty_thirty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_thirteen')
#    twenty_forty_twenty_one_thirty = models.ForeignKey(Profile, limit_choices_to={'student': True}, blank=True, null=True, related_name='class_fourteen')

#    def __str__(self):
#        return str(self.work_date)
