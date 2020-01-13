from django.contrib import admin

from .models import TeacherBillingPeriod, TeacherBillingHours, TeacherBillingRates, \
    TeacherCustomBillingHours, TeacherCustomBillingRates, TeacherTotalBillingHours, \
    TeacherTotalCustomBillingHours, TeacherCumulativeCustomBillingHours, \
    TeacherCumulativeMonthlyPayment, TeacherCumulativeCustomBillingPayment

admin.site.register(TeacherBillingPeriod)
admin.site.register(TeacherBillingHours)
admin.site.register(TeacherBillingRates)
admin.site.register(TeacherCustomBillingHours)
admin.site.register(TeacherCustomBillingRates)
admin.site.register(TeacherTotalBillingHours)
admin.site.register(TeacherTotalCustomBillingHours)
admin.site.register(TeacherCumulativeCustomBillingHours)
admin.site.register(TeacherCumulativeMonthlyPayment)
admin.site.register(TeacherCumulativeCustomBillingPayment)