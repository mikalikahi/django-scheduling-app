from django import forms
from .models import StudentClass, TeacherClass, ClassInformation

class TeacherClassForm(forms.ModelForm):
    class Meta:
        model = TeacherClass
        fields = ('student_class', 'teacher_scheduled', 'hours_billed', 'custom_billing')

    def clean_teacher_scheduled(self):
        this_instance = self.instance
        this_id = this_instance.pk
        student_class = StudentClass.objects.get(pk=this_id)
        if self.cleaned_data['teacher_scheduled'] in student_class.unavailable_teachers() and \
                self.cleaned_data['teacher_scheduled'] != student_class.teacherclass.teacher_scheduled:
            raise forms.ValidationError("That teacher is unavailable")
        return self.cleaned_data['teacher_scheduled']

class ClassInformationForm(forms.ModelForm):
    class Meta:
        model = ClassInformation
        fields = '__all__'

    def clean_location(self):
        this_instance = self.instance
        this_id = this_instance.pk
        student_class = StudentClass.objects.get(pk=this_id)
        if self.cleaned_data['location'] in student_class.unavailable_classroom() and \
                self.cleaned_data['location'] != student_class.classinformation.location:
            raise forms.ValidationError("That classroom is unavailable")
        return self.cleaned_data['location']

    def clean_students_in_attendance(self):
        this_instance = self.instance
        this_id = this_instance.pk
        student_class = StudentClass.objects.get(pk=this_id)
        for student in self.cleaned_data['students_in_attendance']:
            if student.profile not in student_class.students_scheduled():
                raise forms.ValidationError("That student is not scheduled for this class")
        return self.cleaned_data['students_in_attendance']

class UpdateTeacherAttendance(forms.ModelForm):
    class Meta:
        model = ClassInformation
        fields = [
            'teacher_attended',
            'class_content',
        ]

class UpdateStudentAttendance(forms.ModelForm):
    class Meta:
        model = ClassInformation
        fields = [
            'student_attended',
        ]

STUDENT_CLASS_STATUS_CHOICES = (
    ('scheduled', 'Scheduled'),
    ('cancellation_request', 'Cancellation_Request'),
    )

class UpdateClassStatus(forms.ModelForm):
    class_status = forms.ChoiceField(choices=STUDENT_CLASS_STATUS_CHOICES)

    class Meta:
        model = ClassInformation
        fields = [
            'class_status',
            'absence_request_reason',
        ]