from time import strptime

__author__ = 'ipman'

import datetime
#from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.admin.widgets import AdminDateWidget
from claim import models
from django import forms
from django.forms.extras import SelectDateWidget
from django.forms import ModelForm, SplitDateTimeWidget, CheckboxInput, modelformset_factory
from claim.models import support_request, ModelTransmitter, TypeRequest
#from claim.views import date_convert_to_view
from reference_books.models import ExpandedUserProfile, CoWorker, Company, Client

class CustomDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('input_formats', ("%d.%m.%Y",))
        super(CustomDateField, self).__init__(*args, **kwargs)

class get_new_save_request(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(get_new_save_request, self).__init__(*args, **kwargs)
        Company = ExpandedUserProfile.objects.get(UserName=self.user).ServingCompany
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            self.fields['NumObject'].required = False
            self.fields['NumObject'].widget.attrs['disabled'] = 'disabled'
            self.fields['AddressObject'].required = False
            self.fields['AddressObject'].widget.attrs['disabled'] = 'disabled'
            self.fields['FaultAppearance'].required = False
            self.fields['FaultAppearance'].widget.attrs['disabled'] = 'disabled'
            #self.fields['CoWorkers'].required = False
            self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServingCompany=Company,StatusWorking=True)
            self.fields['CoWorkers'].widget.attrs['size'] = 7
        else:
            #self.fields['CoWorkers'].required = False
            self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServingCompany=Company,StatusWorking=True)
            self.fields['Client_bd'].required = False
            self.fields['Client_bd'].widget.attrs['disabled'] = 'disabled'

    Client_bd           = forms.ModelChoiceField(required=False, label='Контрагент', queryset = Client.objects.all(), widget=forms.Select(attrs={'class':'chosen-select', 'placeholder':'Поиск контрагента', 'style':'height:38px', 'tabindex':'2'}))
    DateTime_schedule   = forms.DateField(label='Запланировано на', widget=AdminDateWidget, initial=datetime.date.today)
    DateTime_work       = forms.DateField(required=False, label='Дата выполнения', widget=AdminDateWidget)
    FaultAppearance     = forms.CharField(required=False, label='Неисправность', widget=forms.widgets.Textarea(attrs={'rows':3}))
    DescriptionWorks    = forms.CharField(required=False, label='Сделано', widget=forms.widgets.Textarea(attrs={'rows':3}))
    #CoWorkers           = forms.MultipleChoiceField(label='Исполнители', queryset = CoWorker.objects.filter(ServingCompany=Company,StatusWorking=True), widget=forms.widgets.SelectMultiple(attrs={'rows':5}))
    class Meta:
        model = support_request
        fields = ['NumObject','model_transmitter','num_transmitter','AddressObject','Client',
                  'FaultAppearance','DateTime_schedule','DescriptionWorks','DateTime_work','CoWorkers','Client_bd','Status']

TypeRequest_change = {
    ('trouble_shooting', 'Устранение неисправностей'), ('', 'Новый монтаж'), ('3', 'Доустановка'), ('4', 'Демонтаж'), ('5', 'Техническое обслуживание')
}

class request_per_date(forms.Form):
    request_date       = forms.DateField(label='Дата', initial=datetime.date.today, widget=AdminDateWidget)
    no_range_date      = forms.BooleanField(label='За весь период', required=False, widget=CheckboxInput)
    CoWorkers          = forms.ModelChoiceField(required=False, label="Исполнитель", queryset=models.CoWorker.objects.all(), widget=forms.Select(attrs={'class':'selector'}))
    Status             = forms.ModelChoiceField(required=False, label="Состояние", queryset=models.Status.objects.all(), widget=forms.Select(attrs={'class':'selector'}))
    NumObject          = forms.CharField(required=False, label='Номер объекта', widget=forms.widgets.NumberInput)

class LoginForm(forms.Form):
    username = forms.CharField(label=u'Имя пользователя')
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