from datetime import datetime
from django import template
from django.template.defaultfilters import stringfilter
from build.models import build_request
from claim.models import support_request
from dashboard.models import Menu
from maintenance.models import maintenance_request, objects_to
from reference_books.models import ExpandedUserProfile, Status, CoWorker
from request.settings import *

__author__ = 'ipman'

register = template.Library()


@register.inclusion_tag('templatetags/user_active.html')
def users_active(user):
    user_company = ExpandedUserProfile.objects.get(UserName=user).ServingCompany
    # user = User.is_active
    return {'users': user_company}


@register.inclusion_tag('templatetags/informer_trouble.html')
def informer_trouble(user):
    user_company = ExpandedUserProfile.objects.get(UserName=user).ServingCompany
    list_coworker = CoWorker.objects.filter(ServingCompany=user_company)
    requests_open = support_request.objects.filter(Company=user_company,
                                                   Status=Status.objects.get(slug='open'),
                                                   CoWorkers__isnull=True).count()
    requests_work = support_request.objects.filter(Company=user_company,
                                                   Status=Status.objects.get(slug='open'),
                                                   CoWorkers__in=list_coworker).count()
    requests_control = support_request.objects.filter(Company=user_company,
                                                      Status=Status.objects.get(slug='control')).count()
    return {'requests_open': requests_open, 'requests_work': requests_work, 'requests_control': requests_control}


@register.inclusion_tag('templatetags/informer_build.html')
def informer_build(user):
    user_company = ExpandedUserProfile.objects.get(UserName=user).ServingCompany
    requests_open = build_request.objects.filter(Company=user_company,
                                                 Status=Status.objects.get(slug='open')).count()
    requests_today = build_request.objects.filter(Company=user_company,
                                                  Status=Status.objects.get(slug='open'),
                                                  DateTime_schedule=datetime.today()).count()
    requests_control = build_request.objects.filter(Company=user_company,
                                                    Status=Status.objects.get(slug='control')).count()
    return {'requests_open': requests_open, 'requests_today': requests_today, 'requests_control': requests_control}


@register.inclusion_tag('templatetags/informer_maintenance.html')
def informer_maintenance(user):
    user_company = ExpandedUserProfile.objects.get(UserName=user).ServingCompany
    list_coworker = CoWorker.objects.filter(ServingCompany=user_company)
    list_object = objects_to.objects.filter(ServingCompany=user_company)
    requests_open = maintenance_request.objects.filter(Object__in=list_object,
                                                       Status=Status.objects.get(slug='open'),
                                                       CoWorkers__isnull=True).count()
    requests_work = maintenance_request.objects.filter(Object__in=list_object,
                                                       Status=Status.objects.get(slug='open'),
                                                       CoWorkers__in=list_coworker).count()
    requests_control = maintenance_request.objects.filter(Object__in=list_object,
                                                          Status=Status.objects.get(slug='control')).count()
    return {'requests_open': requests_open, 'requests_work': requests_work, 'requests_control': requests_control}


@register.inclusion_tag('templatetags/menu.html')
def tag_menu(req_user):
    return {'nodes':Menu.objects.all(), 'user':req_user, 'app':NAME_APP, 'scompany':NAME_COMPANY}

@register.filter
@stringfilter
def get_constans(value):
    if value == 'dev_name':
        return DEVELOP_NAME
    elif value == 'dev_email':
        return DEVELOP_EMAIL
    elif value == 'owner':
        return OWNER