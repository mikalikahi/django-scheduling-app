from django.conf.urls import url

from .views import low_hours_list_view, class_billing_detail_view, billing_accounts_list_view

urlpatterns = [
    url(r'^$', billing_accounts_list_view, name='billing-accounts-list'),
    url(r'^low_hours_list/$', low_hours_list_view, name='low-hours'),
    url(r'^(?P<slug>[\w-]+)/billing_detail/$', class_billing_detail_view, name='class-billing-detail'),
]