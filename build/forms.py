from dashboard.templatetags.personal_tags import check_user_in_group

__author__ = 'ipman'

import datetime
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, CheckboxInput
from accounts.views import get_scompany
from build.models import bacts, bproposals
from exploitation.models import eproposals as exploitation_proposal
from reference_books.models import CoWorker, Status, Client, TypeSecurity


class get_new_save_request(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(get_new_save_request, self).__init__(*args, **kwargs)
        Company = get_scompany(self.user)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            self.fields['ServiceCompany'].required = False
            self.fields['ServiceCompany'].widget.attrs['disabled'] = 'disabled'
            self.fields['TypeBuild'].required = False
            self.fields['TypeBuild'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['ServiceCompany'].queryset = Company
            if Company.count() == 1:
                self.fields['ServiceCompany'].initial = Company.first().id
            self.fields['ServiceCompany'].queryset = get_scompany(self.user)
            self.fields['Status'].initial = Status.objects.get(slug='open')

    Client_choices = forms.ModelChoiceField(required=False, label=u'Контрагент', queryset=Client.objects.all(),
                                            widget=forms.Select(attrs={'class': 'chosen-select',
                                                                       'placeholder': 'Поиск контрагента',
                                                                       'style': 'height:38px', 'tabindex': '2'}))
    DateTime_schedule = forms.DateTimeField(label=u'Запланировано на', initial=datetime.date.today,
                                            widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                            input_formats=('%Y-%m-%d',))
    DateTime_work = forms.DateTimeField(required=False, label=u'Дата выполнения',
                                        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                        input_formats=('%Y-%m-%d',))
    DescriptionWorks = forms.CharField(required=False, label=u'Описание',
                                       widget=forms.widgets.Textarea(attrs={'rows': 3}))
    TypeSecurity = forms.ModelMultipleChoiceField(label=u'Тип сигнализации', queryset=TypeSecurity.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple(
                                                      attrs={'style': 'margin-left: .75rem;'}), )
    Status = forms.ModelChoiceField(required=False, label='Состояние',
                                    queryset=Status.objects.filter(view_form=True), widget=forms.Select())

    class Meta:
        model = bproposals
        fields = ['TypeBuild', 'TypeSecurity', 'ServiceCompany', 'Client_choices', 'AddressObject', 'DateTime_schedule',
                  'DescriptionWorks', 'DateTime_work', 'model_transmitter', 'num_transmitter', 'Status']


class get_new_save_acts_build(ModelForm):

    def __init__(self, *args, **kwargs):
        self.proposal_id = kwargs.pop('proposal_id', None)
        super(get_new_save_acts_build, self).__init__(*args, **kwargs)
        scompany = bproposals.objects.get(id=self.proposal_id).ServiceCompany

        self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServiceCompany=scompany, StatusWorking=True). \
            distinct().order_by('Person_FIO')
        self.fields['CoWorkers'].widget.attrs['size'] = '15'

    Day_reporting = forms.DateField(required=True, label='Отчетная дата', initial=datetime.date.today,
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    Description = forms.CharField(required=False, label='Описание',
                                  widget=forms.widgets.Textarea(attrs={'rows': 5}))

    class Meta:
        model = bacts
        fields = ['Day_reporting', 'CoWorkers', 'Description']


class coworkers_range_date(forms.Form):  # Вывести: кто где работал в течении заданного периода и за один день
    acts_date_start = forms.DateField(label='Дата начала', widget=AdminDateWidget, initial=datetime.date.today)
    acts_date_stop = forms.DateField(label='Дата окончания', widget=AdminDateWidget, initial=datetime.date.today)


class coworkers_object(forms.Form):  # Вывести: кто монтировал объект и сколько

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(coworkers_object, self).__init__(*args, **kwargs)

        self.fields['build_request'].queryset = exploitation_proposal.objects.filter(
            Status=Status.objects.get(slug='complete').id,
            Company=get_scompany(self.user))
        self.fields['build_request'].widget.attrs['class'] = 'selector'

    class Meta:
        model = bacts
        fields = ['build_request']


class coworker_range_date(forms.Form):  # Вывести: где работал один исполнитель за период

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(coworker_range_date, self).__init__(*args, **kwargs)

        self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServiceCompany=get_scompany(self.user))

    CoWorkers = forms.ModelChoiceField(queryset=None, empty_label=None, widget=forms.Select())
    acts_date_start = forms.DateField(label='Дата начала', widget=AdminDateWidget, initial=datetime.date.today)
    acts_date_stop = forms.DateField(label='Дата окончания', widget=AdminDateWidget, initial=datetime.date.today)
    no_range_date = forms.BooleanField(label='За весь период', required=False, widget=CheckboxInput)

    class Meta:
        model = CoWorker
        fields = ['CoWorkers']


class build_complete_range_date(forms.Form):  # Вывести: законченые монтажи за период
    work_date_start = forms.DateField(label='Дата начала', widget=AdminDateWidget, initial=datetime.date.today)
    work_date_stop = forms.DateField(label='Дата окончания', widget=AdminDateWidget, initial=datetime.date.today)


