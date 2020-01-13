"""TLI_FLD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^employment/$', TemplateView.as_view(template_name='employment.html'), name='employment'),
    url(r'^info/$', TemplateView.as_view(template_name='info.html'), name='info'),
    url(r'^student-classes/', include('student_classes.urls', namespace='student-classes')),
    url(r'^class-billing-admin/', include('class_billing_admin.urls', namespace='class-billing-admin')),
    url(r'^scheduling/', include('schedule.urls', namespace='scheduling')),
    url(r'^contacts/', include('contacts.urls', namespace='contacts')),
]
