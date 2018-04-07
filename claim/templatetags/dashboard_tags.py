from django import template
from django.contrib.auth.models import User
from django.http import request
from claim.models import support_request
from dashboard.views import custom_proc
from reference_books.models import ExpandedUserProfile, Status

__author__ = 'ipman'

register = template.Library()

@register.inclusion_tag('templatetags/user_active.html')
def users_active(user):
    user_company = ExpandedUserProfile.objects.get(UserName=user).ServingCompany
    #user = User.is_active
    return {'users': user_company}

@register.inclusion_tag('templatetags/informer_trouble.html')
def informer_trouble(user):
    user_company = ExpandedUserProfile.objects.get(UserName=user).ServingCompany
    requests_open = support_request.objects.filter(Company=user_company,Status=Status.objects.get(slug='open')).count()
    requests_work = support_request.objects.filter(Company=user_company,Status=Status.objects.get(slug='open')).count()
    requests_control = support_request.objects.filter(Company=user_company,Status=Status.objects.get(slug='control')).count()
    return {'requests_open': requests_open, 'requests_work': requests_work, 'requests_control': requests_control}

@register.inclusion_tag('templatetags/informer_build.html')
def informer_build(user):
    user_company = ExpandedUserProfile.objects.get(UserName=user).ServingCompany
    requests_open = support_request.objects.filter(Company=user_company,Status=Status.objects.get(slug='open')).count()
    requests_work = support_request.objects.filter(Company=user_company,Status=Status.objects.get(slug='open')).count()
    requests_control = support_request.objects.filter(Company=user_company,Status=Status.objects.get(slug='control')).count()
    return {'requests_open': requests_open, 'requests_work': requests_work, 'requests_control': requests_control}

@register.inclusion_tag('templatetags/informer_maintenance.html')
def informer_maintenance(user):
    user_company = ExpandedUserProfile.objects.get(UserName=user).ServingCompany
    requests_open = support_request.objects.filter(Company=user_company,Status=Status.objects.get(slug='open')).count()
    requests_work = support_request.objects.filter(Company=user_company,Status=Status.objects.get(slug='open')).count()
    requests_control = support_request.objects.filter(Company=user_company,Status=Status.objects.get(slug='control')).count()
    return {'requests_open': requests_open, 'requests_work': requests_work, 'requests_control': requests_control}