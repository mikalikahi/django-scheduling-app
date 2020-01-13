from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

User = get_user_model()

from .models import Profile
from .forms import RegisterForm, UserLoginForm, UpdateProfile

profile = Profile

def profile_model_detail_view(request, id=None):
    current_user = request.user
    object = User.objects.get(username=current_user)
    obj = get_object_or_404(Profile, user=current_user)
    if request.method == 'POST':
        form = UpdateProfile(request.POST or None, instance=obj)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.save()
    else:
        form = UpdateProfile()
    context = {
        "obj": obj,
        "object": object,
        "form": form,
    }
    if request.is_ajax():
        json_obj = model_to_dict(obj)
        json_obj.update({'username': object.username})
        json_obj.update({'email': object.profile.contact_email})
        if obj.teacher == True and obj.student == True:
            json_obj.update({'status': "Teacher and Student"})
        elif obj.teacher == True and obj.student == False:
            json_obj.update({'status': "Teacher"})
        elif obj.teacher == False and obj.student == True:
            json_obj.update({'status': "Student"})
        else:
            json_obj.update({'status': "Please enter status"})
        html = render_to_string('accounts/profile-update-view.html', context, request=request)
        json_obj.update({'form': html})
        return JsonResponse(json_obj)
    template = "accounts/profile-detail-view.html"
    return render(request, template, context)

def student_profile_detail_view(request, id=None):
    current_user = request.user
    obj = get_object_or_404(Profile, id=id)
    context = {
        "object": obj,
    }
    template = "accounts/student-profile-detail-view.html"
    return render(request, template, context)

def register(request, *args, **kwargs):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/accounts/login")
    return render(request, "accounts/register.html", {"form": form})

def user_login(request, *args, **kwargs): # note: don't call it 'login'!
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username_ = form.cleaned_data.get('username')
        user_obj = User.objects.get(username__iexact=username_)
        login(request, user_obj)
        return HttpResponseRedirect("/")
    return render(request, "accounts/login.html", {"form": form})

def user_logout(request): #note: can't use logout as function name
    logout(request)
    return HttpResponseRedirect("/accounts/login")
