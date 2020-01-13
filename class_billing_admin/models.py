from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import Profile
from .utils import random_string_generator

class StudentBillingManager(models.Manager):
    def under_two_hours(self):
        return [account for account in self.get_queryset() if account.purchased_class_hours <= 2]

    def student_email_under_two_hours(self):
        accounts = [account for account in self.get_queryset() if account.purchased_class_hours <= 2]
        account_dict = {}
        for account in accounts:
            account_dict.update({account: [account.contact_email for account in account.student_account.all()]})
        return account_dict

class StudentBilling(models.Model):
    custom_query = StudentBillingManager()
    objects = models.Manager()
    student_account = models.ManyToManyField(Profile, limit_choices_to={'student': True},
                                               related_name='student_account')
    purchased_class_hours = models.DecimalField(max_digits=5, decimal_places=2)
    account_id = models.CharField(max_length=10, null=True, blank=True)
    slug = models.SlugField(max_length=50, blank=True, null=True)

    def __str__(self):
        sb = [student.user.username for student in self.student_account.all()]
        students_billed = ', '.join(sb)
        return "Billing for {}".format(students_billed)

@receiver(pre_save, sender=StudentBilling)
def pre_save_account_id(sender, **kwargs):
    random_string = random_string_generator()
    slug = random_string
    kwargs['instance'].account_id = random_string
    kwargs['instance'].slug = slug