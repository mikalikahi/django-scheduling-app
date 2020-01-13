from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from accounts.models import Profile
from class_billing_admin.models import StudentBilling

class TeacherBillingPeriod(models.Model):
    start_date = models.DateField()
    finish_date = models.DateField()

    def __str__(self):
        return 'Billing period from {} to {}'.format(self.start_date, self.finish_date)

class TeacherBillingHours(models.Model):
    billing = models.ForeignKey(TeacherBillingPeriod, related_name='billing_hours', blank=True, null=True)
    teacher_billed = models.ForeignKey(Profile, limit_choices_to={'teacher': True}, blank=True, null=True)
    billed_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    outside_billed_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return "Billing hours for {} from {} to {}".format(self.teacher_billed, self.billing.start_date, self.billing.finish_date)

    class Meta:
        verbose_name_plural = 'Student Billing Hourse'

class TeacherTotalBillingHours(models.Model):
    teacher_billing_hours = models.OneToOneField(TeacherBillingHours, on_delete=models.CASCADE, primary_key=True)
    total_billed_inside_hours = models.PositiveIntegerField(default=0)
    total_billed_outside_hours = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Total Standard Payment for {} from {} to {}'.format(self.teacher_billing_hours.teacher_billed, \
                                                                    self.teacher_billing_hours.billing.start_date, \
                                                                    self.teacher_billing_hours.billing.finish_date)

    class Meta:
        verbose_name_plural = 'Teacher Total Billing Hours'

class TeacherCumulativeMonthlyPayment(models.Model):
    paid_teacher = models.ForeignKey(Profile, limit_choices_to={'teacher': True}, related_name='teacher_paid')
    payment_period = models.ForeignKey(TeacherBillingPeriod, related_name='payment_period')
    total_cumulative_payment = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Total Cumulative Monthly Payment for {} from {} to {}'.format(self.paid_teacher, \
                                                                             self.payment_period.start_date, \
                                                                             self.payment_period.finish_date)

    class Meta:
        verbose_name_plural = 'Teacher Cumulative Monthly Payments'

class TeacherCumulativeCustomBillingHours(models.Model):
    custom_billing = models.ManyToManyField('TeacherCustomBillingHours', related_name='custom_billing_accounts', blank=True)
    teacher_billed = models.ForeignKey(Profile, limit_choices_to={'teacher': True}, related_name='teacher_billed')
    billing_hours_period = models.ForeignKey(TeacherBillingPeriod, related_name='billing_period')

    def __str__(self):
        return 'All custom billing accounts for {} from {} to {}'.format(self.teacher_billed, self.billing_hours_period.start_date, \
                                                                         self.billing_hours_period.finish_date)

    class Meta:
        verbose_name_plural = 'Teacher Cumulative Monthly Billing Hours'

class TeacherCumulativeCustomBillingPayment(models.Model):
    cumulative_custom_billing_hours = models.OneToOneField(TeacherCumulativeCustomBillingHours, \
                                                           related_name='cumulative_custom_billing')
    total_custom_cumulative_payment = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Cumulative payment total for {}'.format(self.cumulative_custom_billing_hours)

    class Meta:
        verbose_name_plural = 'Teacher Cumulative Monthly Billing Payments'

class TeacherCustomBillingHours(models.Model):
    billing = models.ForeignKey(TeacherBillingPeriod, related_name='teacher_billing_hours', blank=True, null=True)
    teacher_billed = models.ForeignKey(Profile, limit_choices_to={'teacher': True}, blank=True, null=True)
    billed_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    account = models.ForeignKey(StudentBilling)

    def __str__(self):
        return "Billing hours for {} with account {} from {} to {}".format(self.teacher_billed, self.account, \
                                                                           self.billing.start_date, self.billing.finish_date)

    class Meta:
        verbose_name_plural = 'Teacher Custom Billing Hours'

class TeacherTotalCustomBillingHours(models.Model):
    teacher_custom_billing_hours = models.OneToOneField(TeacherCustomBillingHours, on_delete=models.CASCADE, primary_key=True)
    total_billed_custom_hours = models.PositiveIntegerField(default=0)

    def __str__(self):
        sb = [student.user.username for student in self.teacher_custom_billing_hours.account.student_account.all()]
        students_billed = ', '.join(sb)
        return 'Total Custom Payment for {} with account {} from {} to {}'.format(self.teacher_custom_billing_hours.teacher_billed, \
                                                                                  students_billed, \
                                                                                  self.teacher_custom_billing_hours.billing.start_date, \
                                                                                  self.teacher_custom_billing_hours.billing.finish_date)

    class Meta:
        verbose_name_plural = 'Teacher Total Custom Billing Hours'


class TeacherBillingRates(models.Model):
    teacher_billed = models.OneToOneField(Profile, limit_choices_to={'teacher': True}, unique=True, blank=True, null=True)
    inside_hourly = models.PositiveSmallIntegerField(blank=True, null=True)
    outside_hourly = models.PositiveSmallIntegerField(blank=True, null=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Billing rates for {}".format(self.teacher_billed)

    class Meta:
        verbose_name_plural = 'Teacher Billing Rates'

class TeacherCustomBillingRatesManager(models.Manager):
    def get_customized_accounts(self):
        customized_accounts_query = [custom_billing.account for custom_billing in self.get_queryset()]
        return customized_accounts_query

class TeacherCustomBillingRates(models.Model):
    objects = models.Manager()
    custom_query = TeacherCustomBillingRatesManager()
    teacher_billed = models.ForeignKey(Profile, limit_choices_to={'teacher': True}, blank=True, null=True)
    hourly = models.PositiveSmallIntegerField(blank=True, null=True)
    account = models.ForeignKey(StudentBilling)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Billing rates for {} with account: {}".format(self.teacher_billed, self.account)

    class Meta:
        verbose_name_plural = 'Teacher Custom Billing Rates'

def post_save_teacher_total_billing_hours_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            TeacherTotalBillingHours.objects.create(teacher_billing_hours=instance)
        except:
            pass
    else:
        total_tuple = TeacherTotalBillingHours.objects.get_or_create(teacher_billing_hours=instance)
        total_billing_obj = total_tuple[0]
        inside_hours = total_billing_obj.teacher_billing_hours.billed_hours
        if inside_hours == None:
            inside_hours = 0
        inside_hourly_rate = total_billing_obj.teacher_billing_hours.teacher_billed.teacherbillingrates.inside_hourly
        total_billing_obj.total_billed_inside_hours = inside_hours * inside_hourly_rate
        outside_hours = total_billing_obj.teacher_billing_hours.outside_billed_hours
        if outside_hours == None:
            outside_hours = 0
        outside_hourly_rate = total_billing_obj.teacher_billing_hours.teacher_billed.teacherbillingrates.outside_hourly
        total_billing_obj.total_billed_outside_hours = outside_hours * outside_hourly_rate
        total_billing_obj.save()
post_save.connect(post_save_teacher_total_billing_hours_receiver, sender=TeacherBillingHours)

def post_save_teacher_total_custom_billing_hours_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            TeacherTotalCustomBillingHours.objects.create(teacher_custom_billing_hours=instance)
        except:
            pass
    else:
        total_billing_obj = TeacherTotalCustomBillingHours.objects.get_or_create(teacher_custom_billing_hours=instance)[0]
        print('This is the where total amount of hours billed is coming from {}'.format(total_billing_obj.teacher_custom_billing_hours))
        total_hours = total_billing_obj.teacher_custom_billing_hours.billed_hours
        if total_hours == None:
            total_hours = 0
        print('This is the total hours billed for the month {}'.format(total_hours))
        hourly_rate_account = total_billing_obj.teacher_custom_billing_hours.account
        print('This is the account {}'.format(hourly_rate_account))
        hourly_rate_obj = TeacherCustomBillingRates.objects.filter(account=hourly_rate_account)[0]
        print(hourly_rate_obj)
        hourly_rate = hourly_rate_obj.hourly
        print(hourly_rate)
        total_billing_obj.total_billed_custom_hours = total_hours * hourly_rate
        print('This is the amount in the account {}'.format(total_billing_obj.total_billed_custom_hours))
        total_billing_obj.save()
post_save.connect(post_save_teacher_total_custom_billing_hours_receiver, sender=TeacherCustomBillingHours)

def post_save_teacher_cumulative_total_custom_billing_hours_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            TeacherCumulativeCustomBillingHours.objects.create(teacher_billed=instance.teacher_custom_billing_hours.teacher_billed, \
                                                               billing_hours_period=instance.teacher_custom_billing_hours.billing)
        except:
            pass
    else:
        cumulative_billing_obj = TeacherCumulativeCustomBillingHours.objects.get_or_create(teacher_billed=instance.teacher_custom_billing_hours.teacher_billed, \
                                                               billing_hours_period=instance.teacher_custom_billing_hours.billing)[0]
        print(cumulative_billing_obj)
        cumulative_billing_obj.custom_billing.add(instance.teacher_custom_billing_hours)
        cumulative_billing_obj.save()
        print(cumulative_billing_obj.custom_billing.all())
post_save.connect(post_save_teacher_cumulative_total_custom_billing_hours_receiver, sender=TeacherTotalCustomBillingHours)

def post_save_teacher_cumulative_total_custom_payment_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            TeacherCumulativeCustomBillingPayment.objects.create(cumulative_custom_billing_hours=instance)
        except:
            pass
    else:
        cumulative_custom_payment_obj = TeacherCumulativeCustomBillingPayment.objects.get_or_create(cumulative_custom_billing_hours=instance)[0]
        payment_total_list = [payment_obj.pk for payment_obj in cumulative_custom_payment_obj.cumulative_custom_billing_hours.custom_billing.all()]
        print(payment_total_list)
        payment_total_amounts_list = []
        for p_key in payment_total_list:
            added_payment_obj = TeacherTotalCustomBillingHours.objects.get(pk=p_key)
            payment_total_amounts_list.append(added_payment_obj.total_billed_custom_hours)
        print(payment_total_amounts_list)
        sum_numbers = 0
        for x in payment_total_amounts_list:
            sum_numbers += x
        print(sum_numbers)
        cumulative_custom_payment_obj.total_custom_cumulative_payment = sum_numbers
        cumulative_custom_payment_obj.save()
post_save.connect(post_save_teacher_cumulative_total_custom_payment_receiver, sender=TeacherCumulativeCustomBillingHours)

def post_save_teacher_total_billing_hours_receiver_from_regular_hours(sender, instance, created, *args, **kwargs):
    if created:
        try:
            TeacherCumulativeMonthlyPayment.objects.create(paid_teacher=instance.teacher_billing_hours.teacher_billed, \
                                                           payment_period=instance.teacher_billing_hours.billing)
        except:
            pass
    else:
        total_billing_obj = TeacherCumulativeMonthlyPayment.objects.get_or_create(paid_teacher=instance.teacher_billing_hours.teacher_billed, \
                                                                                  payment_period=instance.teacher_billing_hours.billing)[0]
        total_regular_monthly_payment = instance.total_billed_inside_hours + instance.total_billed_outside_hours
        total_billing_hours_obj = TeacherCumulativeCustomBillingHours.objects.get_or_create(billing_hours_period=instance.teacher_billing_hours.billing, \
                                                                                            teacher_billed=instance.teacher_billing_hours.teacher_billed)[0]
        total_billing_hours_obj.save()
        total_custom_payment_obj = TeacherCumulativeCustomBillingPayment.objects.get_or_create(pk=total_billing_hours_obj.pk)[0]
        total_custom_payment_obj.save()
        total_custom_monthly_payment = total_custom_payment_obj.total_custom_cumulative_payment
        print(total_custom_monthly_payment)
        total_billing_obj.total_cumulative_payment = total_regular_monthly_payment + total_custom_monthly_payment
        total_billing_obj.save()
        print(total_billing_obj.total_cumulative_payment)
post_save.connect(post_save_teacher_total_billing_hours_receiver_from_regular_hours, sender=TeacherTotalBillingHours)

def post_save_teacher_total_billing_hours_receiver_from_custom_hours(sender, instance, created, *args, **kwargs):
    if created:
        try:
            TeacherCumulativeMonthlyPayment.objects.create(paid_teacher=instance.cumulative_custom_billing_hours.teacher_billed, \
                                                           payment_period=instance.cumulative_custom_billing_hours.billing_hours_period)
        except:
            pass
    else:
        teacher_billing_obj = instance.cumulative_custom_billing_hours.teacher_billed
        payment_period_obj = instance.cumulative_custom_billing_hours.billing_hours_period
        print(teacher_billing_obj)
        print(payment_period_obj)
        total_billing_obj = TeacherCumulativeMonthlyPayment.objects.filter(paid_teacher= teacher_billing_obj,
                                                           payment_period=payment_period_obj).first()
        print('This is total_billing_obj: {}'.format(total_billing_obj))

        total_regular_billing_pk_obj = TeacherBillingHours.objects.get_or_create(billing=instance.cumulative_custom_billing_hours.billing_hours_period, \
                                                                                 teacher_billed=instance.cumulative_custom_billing_hours.teacher_billed)[0]
        print(total_regular_billing_pk_obj)
        total_regular_billing_obj = TeacherTotalBillingHours.objects.get_or_create(pk=total_regular_billing_pk_obj.pk)[0]
        total_custom_monthly_payment = instance.total_custom_cumulative_payment
        print(total_custom_monthly_payment)
        total_regular_monthly_payment = total_regular_billing_obj.total_billed_inside_hours + total_regular_billing_obj.total_billed_outside_hours
        total_billing_obj.total_cumulative_payment = total_regular_monthly_payment + total_custom_monthly_payment
        total_billing_obj.save()
        print('This is the total: {}'.format(total_billing_obj.total_cumulative_payment))
post_save.connect(post_save_teacher_total_billing_hours_receiver_from_custom_hours, sender=TeacherCumulativeCustomBillingPayment)