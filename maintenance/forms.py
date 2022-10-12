import datetime

from django import forms
from django.db.models import Q
from django.forms import ModelForm, CheckboxInput

from maintenance.models import mobjects, mproposals, mtroubles
from reference_books.models import CoWorker, Client, RoutesMaintenance, Month_list, TypeSecurity, Status
from accounts.views import get_scompany, get_cur_scompany

__author__ = 'ipman'


class get_add_request_to(ModelForm):

    def __init__(self, *args, **kwargs):
        self.object_id = kwargs.pop('object_id', None)
        super(get_add_request_to, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        scompany = mobjects.objects.get(id=self.object_id).ServiceCompany

        if instance and instance.id:
            self.fields['CoWorkers'].queryset = CoWorker.objects. \
                filter(Q(StatusWorking=True) | Q(id__in=instance.CoWorkers.all()),
                       ServiceCompany=scompany).distinct().order_by('Person_FIO')
        else:
            self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServiceCompany=scompany, StatusWorking=True). \
                distinct().order_by('Person_FIO')
            self.fields['Status'].initial = Status.objects.get(slug='open')

        self.fields['CoWorkers'].widget.attrs['size'] = '10'

    DateTime_schedule = forms.DateField(label='Запланировано на',
                                        initial=datetime.date.today, input_formats=('%Y-%m-%d',),
                                        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    DateTime_work = forms.DateField(required=False, label='Дата выполнения', input_formats=('%Y-%m-%d',),
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    DescriptionWorks = forms.CharField(required=False, label='Сделано',
                                       widget=forms.widgets.Textarea(attrs={'rows': 4}))
    create_support_request = forms.BooleanField(label='Создать заявку в "Эксплуатации"',
                                                required=False, widget=CheckboxInput)
    Status = forms.ModelChoiceField(required=False, label='Состояние', widget=forms.Select(),
                                    queryset=Status.objects.filter(view_form=True))

    class Meta:
        model = mproposals
        fields = ['DateTime_schedule', 'DescriptionWorks', 'DateTime_work', 'CoWorkers', 'Status']


class get_add_object_to(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(get_add_object_to, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            self.fields['Routes'].required = False
            self.fields['Routes'].queryset = RoutesMaintenance.objects.filter(
                ServiceCompany__in=get_scompany(self.user))
            self.fields['ServiceCompany'].required = False
            self.fields['ServiceCompany'].widget.attrs['disabled'] = 'disabled'
            self.fields['Client_choices'].required = False
            self.fields['Client_choices'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['Routes'].queryset = RoutesMaintenance.objects.filter(
                ServiceCompany__in=get_scompany(self.user))

    Client_choices = forms.ModelChoiceField(required=False, label=u'Контрагент', queryset=Client.objects.all(),
                                            widget=forms.Select(
                                                attrs={'class': 'chosen-select', 'placeholder': 'Поиск контрагента',
                                                       'style': 'height:38px', 'tabindex': '2'}))
    Date_open = forms.DateField(required=False, label='Дата начала', initial=datetime.datetime.today(),
                                widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                input_formats=('%Y-%m-%d',))
    Date_end = forms.DateField(required=False, label='Дата окончания',
                               help_text='Указываем последний день обслуживания',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    TypeSecurity = forms.ModelMultipleChoiceField(label=u'Тип сигнализации',
                                                  widget=forms.CheckboxSelectMultiple(
                                                      attrs={'style': 'margin-left: .75rem;'}),
                                                  queryset=TypeSecurity.objects.all())
    Month_schedule = forms.ModelMultipleChoiceField(label=u'Месяцы обслуживания',
                                                    widget=forms.CheckboxSelectMultiple(
                                                        attrs={'style': 'margin-left: .75rem;'}),
                                                    queryset=Month_list.objects.all().order_by('id'))

    class Meta:
        model = mobjects
        fields = ['NumObject', 'AddressObject', 'Routes', 'Client_choices', 'ServiceCompany',
                  'TypeSecurity', 'Month_schedule', 'Date_open', 'Date_end', 'Status_object']


class get_request_routs(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(get_request_routs, self).__init__(*args, **kwargs)
        self.fields['routs'].queryset = RoutesMaintenance.objects.filter(ServiceCompany=get_cur_scompany(self.user))

    month_list = forms.ModelChoiceField(label="Месяц ТО", queryset=Month_list.objects.all(),
                                        initial=datetime.date.today().month,
                                        widget=forms.Select(attrs={'class': 'selector'}))
    year_list = forms.ChoiceField(label="Год", choices=((str(x), x) for x in range(2018, datetime.datetime.now().year+1)),
                                  initial=datetime.datetime.today().year, widget=forms.Select(attrs={'class': 'selector'}))
    routs = forms.ModelChoiceField(label="Маршрут", queryset=RoutesMaintenance.objects.all(),
                                   widget=forms.Select(attrs={'class': 'selector'}))


class request_status_filter(forms.Form):
    month_list = forms.ModelChoiceField(required=False, label="Месяц ТО",
                                        queryset=Month_list.objects.all().order_by('id'),
                                        initial=datetime.date.today().month,
                                        widget=forms.Select(attrs={'class': 'selector'}))
    address = forms.CharField(required=False, label='Адрес объекта', widget=forms.widgets.TextInput)


STATUS_OBJECT_CHOICES = (
    (True, u'Обслуживается'),
    (False, u'Не обслуживается'),
)


class maintenance_object_status(forms.Form):
    object_status = forms.ChoiceField(required=False, label="Статус", choices=STATUS_OBJECT_CHOICES,
                                      widget=forms.Select(attrs={'class': 'selector'}))


class get_add_trouble_form(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(get_add_trouble_form, self).__init__(*args, **kwargs)
        Company = get_scompany(self.user)
        Company_cur = get_cur_scompany(self.user)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            self.fields['AddressObject'].required = False
            self.fields['AddressObject'].widget.attrs['disabled'] = 'disabled'
            self.fields['FaultAppearance'].required = False
            self.fields['FaultAppearance'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['Status'].initial = Status.objects.get(slug='open')

        self.fields['Routes'].queryset = RoutesMaintenance.objects.filter(ServiceCompany=Company_cur)

        self.fields['ServiceCompany'].queryset = Company
        self.fields['ServiceCompany'].initial = Company_cur.id
        self.fields['ServiceCompany'].required = False
        self.fields['ServiceCompany'].widget.attrs['disabled'] = 'disabled'

        self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServiceCompany=Company_cur,
                                                                    StatusWorking=True).distinct()
        self.fields['CoWorkers'].widget.attrs['size'] = 7

    Client_choices = forms.ModelChoiceField(required=False, label=u'Контрагент', queryset=Client.objects.all(),
                                            widget=forms.Select(attrs={'class': 'chosen-select',
                                                                       'placeholder': 'Поиск контрагента',
                                                                       'style': 'height:38px', 'tabindex': '2'}))
    DateTime_work = forms.DateField(required=False, label='Дата выполнения', input_formats=('%Y-%m-%d',),
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    FaultAppearance = forms.CharField(required=False, label='Неисправность',
                                      widget=forms.widgets.Textarea(attrs={'rows': 3}))
    DescriptionWorks = forms.CharField(required=False, label='Сделано',
                                       widget=forms.widgets.Textarea(attrs={'rows': 3}))
    Status = forms.ModelChoiceField(required=False, label='Состояние', widget=forms.Select(),
                                    queryset=Status.objects.filter(view_form=True))

    class Meta:
        model = mtroubles
        fields = ['ServiceCompany', 'AddressObject', 'Client_words', 'FaultAppearance', 'DescriptionWorks',
                  'DateTime_work', 'CoWorkers', 'Client_choices', 'Routes', 'Status']

    def clean(self):
        cleaned_data = super(get_add_trouble_form, self).clean()
        client1 = cleaned_data.get('Client_choices')
        client2 = cleaned_data['Client_words']

        if not self.errors:
            if client1 is None and client2 is None:
                raise forms.ValidationError(u'Заполните одно из полей "Контрагент"')

        return cleaned_data
