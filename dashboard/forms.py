import re
from datetime import datetime, timedelta
from django.forms import CheckboxInput, ModelForm, DateField, DateInput, ModelChoiceField
from accounts.models import Profile
from accounts.views import get_cur_scompany
from reference_books import models
from reference_books.models import CoWorker, TypeRequest, Event, ServiceCompanies

__author__ = 'ipman'

from django.contrib.auth import authenticate
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label=u'Логин')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if not self.errors:
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user is None:
                raise forms.ValidationError(u'Имя пользователя и пароль не подходят')
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user or None


type_request = (
    ('exploitation', u'Эксплуатация'),
    ('build', u'Монтаж'),
    ('maintenance', u'Техническое обслуживание')
)

SET = (
    ('requests', u'только заявки'),
    ('objects', u'только объекты'),
    ('all', u'заявки и объекты')
)

type_date = (
    ('schedule', u'Запланировано'),
    ('work', u'Завершено'),
)


class search_form(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(search_form, self).__init__(*args, **kwargs)
        self.fields['coworkers'].queryset = CoWorker.objects.filter(ServiceCompany=get_cur_scompany(self.user),
                                                                    StatusWorking=True)

    startdate = forms.DateField(label=u'Дата', initial=datetime.today, required=False,
                                widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                input_formats=('%Y-%m-%d',))
    enddate = forms.DateField(label=u'Дата', required=False,
                              widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                              input_formats=('%Y-%m-%d',))
    norangedate = forms.BooleanField(label=u'За весь период', required=False, widget=CheckboxInput)
    typerequest = forms.ChoiceField(label=u'Тип заявки', choices=type_request, widget=forms.Select, required=False)
    typedates = forms.ChoiceField(label=u'Тип дат', choices=type_date, widget=forms.Select, required=False)
    set = forms.ChoiceField(label=u'Набор', choices=SET, widget=forms.Select, required=False)
    coworkers = forms.ModelChoiceField(label=u'Исполнитель', required=False, queryset=models.CoWorker.objects.all(),
                                       widget=forms.Select(attrs={'class': 'selector'}))
    clients = forms.CharField(label=u'Клиент', required=False, widget=forms.widgets.TextInput)

    status = forms.ModelChoiceField(label=u'Состояние', required=False, queryset=models.Status.objects.all(),
                                    widget=forms.Select(attrs={'class': 'selector'}))
    # adrobject = forms.CharField(label=u'Адрес', required=False, widget=forms.widgets.TextInput)
    numobject = forms.CharField(label=u'Номер', required=False, widget=forms.widgets.TextInput)
    adrobject = forms.CharField(label=u'Адрес', required=False, widget=forms.widgets.TextInput)

    def clean(self):
        cleaned_data = super(search_form, self).clean()
        norangedate = cleaned_data['norangedate']
        startdate = cleaned_data['startdate']
        enddate = cleaned_data['enddate']
        numobject = cleaned_data['numobject']

        if norangedate is False:
            if startdate is None:
                self._errors['startdate'] = self.error_class([u'Введите дату поиска'])
            if enddate is not None and enddate < startdate:
                self._errors['enddate'] = self.error_class([u'Дата окончания периода должна быть позже даты начала'])
        if re.findall(r'[ _/.,]', numobject):
            self._errors['numobject'] = self.error_class([u'В номере объекта могут использоваться только цифры и буквы, без пробелов и других символов'])
        return cleaned_data


class select_current_scompany_form(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.scompany = kwargs.pop('scompany', None)
        super(select_current_scompany_form, self).__init__(*args, **kwargs)

        self.fields['scompany'].widget = forms.Select(attrs={'class': 'selector'})
        self.fields['scompany'].queryset = Profile.objects.get(user=self.user).scompany.all()
        self.fields['scompany'].initial = self.scompany

    class Meta:
        model = Profile
        fields = ['scompany']


class events_form(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(events_form, self).__init__(*args, **kwargs)
        # self.fields['filter_scompany'].queryset = Profile.objects.get(user=self.user).scompany.all()

    filter_app = forms.ModelMultipleChoiceField(required=True, label="Разделы",
                                                queryset=TypeRequest.objects.all(),
                                                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check mr-1',
                                                                                           'checked': 'checked',
                                                                                           'onchange': 'checkboxes()'}))
    filter_start_date = DateField(required=True, label=u'Дата ', input_formats=('%Y-%m-%d',), initial=timedelta(days=-1),
                                  widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    filter_end_date = DateField(required=False, label=u'Дата ', input_formats=('%Y-%m-%d',),
                                widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    filter_typeevent = ModelChoiceField(required=False, label="Событие", queryset=Event.objects.filter(forfilter=True),
                                        widget=forms.Select(attrs={'class': 'selector'}))
    filter_scompany = forms.ModelChoiceField(label=u'Сервисная компания', queryset=ServiceCompanies.objects.all(),
                                             widget=forms.Select(attrs={'class': 'selector'}))
