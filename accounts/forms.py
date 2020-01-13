from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import Profile

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
#        the_user = authenticate(username=username, password=password) # Buit in way to authenticate for standard user model
#        if not the_user:
 #           raise forms.ValidationError("Invalid credentials")
        user_obj = User.objects.filter(username=username).first() # the only object for that user
        if not user_obj:
            raise forms.ValidationError("Invalid credentials") #invalid username
        else:
            if not user_obj.check_password(password): #checks for correct password
                #log auth tries
                raise forms.ValidationError("Invalid credentials") #invalid password
        return super(UserLoginForm, self).clean(*args, **kwargs)

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',) #can add email (possibly other fields)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'surname',
            'given_name',
            'contact_email',
            'teacher',
            'student',
            'course_content_preferences',
            'other_personal_information'
        ]