import datetime
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, CheckboxSelectMultiple, CheckboxInput
from django.forms.extras import SelectDateWidget
from maintenance.models import objects_to, maintenance_request, Status_object, trouble_shooting
from reference_books import models
from reference_books.models import ExpandedUserProfile, CoWorker, Client, RoutesMaintenance

__author__ = 'ipman'

now_date = datetime.date.today()
cur_month = now_date.month
cur_year = now_date.year

MONTHS = {
    ('1', 'январь'), ('2', 'февраль'), ('3', 'март'), ('4', 'апрель'), ('5', 'май'), ('6', 'июнь'),
    ('7', 'июль'), ('8', 'август'), ('9', 'сентябрь'), ('10', 'октябрь'), ('11', 'ноябрь'), ('12', 'декабрь')
}

class get_new_save_request(ModelForm):
    DateTime_schedule = forms.DateField(label='Запланировано на', widget=AdminDateWidget, initial=datetime.date.today)
    DateTime_work = forms.DateField(required=False, label='Дата выполнения', widget=AdminDateWidget)
    DescriptionWorks = forms.CharField(required=False, label='Сделано', widget=forms.widgets.Textarea(attrs={'rows':3}))
    create_support_request = forms.BooleanField(label='Создать заявку в разделе "Неисправности"', required=False, widget=CheckboxInput)
    #CoWorkers = forms.MultipleChoiceField(label='Исполнители', widget=forms.widgets.SelectMultiple(attrs={'rows':5}))
    class Meta:
        model = maintenance_request
        fields = ['DateTime_schedule','DescriptionWorks','DateTime_work','CoWorkers','Status']

class get_add_object_to(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(get_add_object_to, self).__init__(*args, **kwargs)
        Company = ExpandedUserProfile.objects.get(UserName=self.user).ServingCompany
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            self.fields['Routes'].required = False
            self.fields['Routes'].queryset = RoutesMaintenance.objects.filter(ServingCompany=Company)
        else:
            self.fields['Routes'].queryset = RoutesMaintenance.objects.filter(ServingCompany=Company)

    Date_open  = forms.DateField(required=False, label='Дата начала', widget=AdminDateWidget)               #years=range(2010,cur_year+1)))
    Date_close = forms.DateField(required=False, label='Дата окончания', help_text='Указываем последний день обслуживания', widget=AdminDateWidget)
    class Meta:
        model = objects_to
        fields = ['NumObject', 'AddressObject', 'Routes', 'Date_open', 'Client', 'ServingCompany', 'TypeSecurity', 'Month_schedule', 'Date_close', 'Status']

class request_maintenance_per_month(forms.Form):
    month_list = forms.ModelChoiceField(required=False, label="Месяц ТО", queryset=models.Month_list.objects.all(), initial=cur_month, widget=forms.Select(attrs={'class':'selector'}))
    routs      = forms.ModelChoiceField(required=False, label="Маршрут", queryset=models.RoutesMaintenance.objects.all(), widget=forms.Select(attrs={'class':'selector'}))

class request_status_filter(forms.Form):
    month_list = forms.ModelChoiceField(required=False, label="Месяц ТО", queryset=models.Month_list.objects.all(), initial=cur_month, widget=forms.Select(attrs={'class':'selector'}))
    address    = forms.CharField(required=False, label='Адрес объекта', widget=forms.widgets.TextInput)

class maintenance_object_status(forms.Form):
    status = Status_object.objects.get(slug='open')
    object_status = forms.ModelChoiceField(required=False, label="Статус", queryset=Status_object.objects.all(), initial=status.id, widget=forms.Select(attrs={'class':'selector'}))

class get_add_trouble_shooting_form(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(get_add_trouble_shooting_form, self).__init__(*args, **kwargs)
        Company = ExpandedUserProfile.objects.get(UserName=self.user).ServingCompany
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            self.fields['AddressObject'].required = False
            self.fields['AddressObject'].widget.attrs['disabled'] = 'disabled'
            self.fields['FaultAppearance'].required = False
            self.fields['FaultAppearance'].widget.attrs['disabled'] = 'disabled'
            self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServingCompany=Company,StatusWorking=True)
            self.fields['CoWorkers'].widget.attrs['size'] = 7
            self.fields['Routes'].required = False
            self.fields['Routes'].queryset = RoutesMaintenance.objects.filter(ServingCompany=Company)
        else:
            self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServingCompany=Company,StatusWorking=True)
            self.fields['Client_bd'].required = False
            self.fields['Client_bd'].widget.attrs['disabled'] = 'disabled'
            self.fields['Routes'].required = False

    Client_bd           = forms.ModelChoiceField(required=False, label='Контрагент', queryset = Client.objects.all(), widget=forms.Select(attrs={'class':'chosen-select', 'placeholder':'Поиск контрагента', 'style':'height:38px', 'tabindex':'2'}))
    DateTime_work       = forms.DateField(required=False, label='Дата выполнения', widget=AdminDateWidget)
    FaultAppearance     = forms.CharField(required=False, label='Неисправность', widget=forms.widgets.Textarea(attrs={'rows':3}))
    DescriptionWorks    = forms.CharField(required=False, label='Сделано', widget=forms.widgets.Textarea(attrs={'rows':3}))
    class Meta:
        model = trouble_shooting
        fields = ['AddressObject','Client_words','FaultAppearance','DescriptionWorks','DateTime_work','CoWorkers','Client_bd','Routes','Status']