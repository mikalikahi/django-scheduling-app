from django.contrib import admin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from .models import StudentClass, TeacherClass, ClassInformation
from .forms import TeacherClassForm, ClassInformationForm

class TeacherClassAdmin(admin.ModelAdmin):
    form = TeacherClassForm

class ClassInformationAdmin(admin.ModelAdmin):
    form = ClassInformationForm
    search_fields = ('class_status',)

class TeacherClassLine(admin.TabularInline):
    model = TeacherClass
    fields = ('teacher_scheduled', 'hours_billed', 'custom_billing')
    classes = ('collapse',)

class ClassInfoLine(admin.TabularInline):
    model = ClassInformation
    fields = ('class_status', 'location',)
    classes = ('collapse',)

class StudentClassAdmin(admin.ModelAdmin):
    list_display = ('students_scheduled_list', 'scheduled_date', 'scheduled_time', 'schedule_time_finish',)
    list_filter = (
        ('scheduled_date', DateRangeFilter),
    )
    date_hierarchy = 'scheduled_date'
    inlines = (TeacherClassLine, ClassInfoLine)
    filter_horizontal = ('student_scheduled',)
    fieldsets = (
        ('Scheduled Students', {
            'fields': ('student_scheduled',),
            'description': 'Select One or More Students',
        }),
        ('Class Time', {
            'fields': ('scheduled_date',
                       ('scheduled_time', 'schedule_time_finish')),
        }),
    )

admin.site.register(StudentClass, StudentClassAdmin)
admin.site.register(TeacherClass, TeacherClassAdmin)
admin.site.register(ClassInformation, ClassInformationAdmin)