__author__ = 'ipman'

import datetime
from django.contrib.auth import authenticate
from django.contrib.admin.widgets import AdminDateWidget
from claim import models
from django import forms
from django.forms import ModelForm, CheckboxInput
from claim.models import support_request
from reference_books.models import ExpandedUserProfile, CoWorker, Client


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
            self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServingCompany=Company,StatusWorking=True)
            self.fields['CoWorkers'].widget.attrs['size'] = 7

            if instance.Required_act == False:
                self.fields['Date_act'].required = False
                self.fields['Date_act'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServingCompany=Company,StatusWorking=True)
            self.fields['Client_bd'].required = False
            self.fields['Client_bd'].widget.attrs['disabled'] = 'disabled'

    Client_bd           = forms.ModelChoiceField(required=False, label='Контрагент', queryset = Client.objects.all(),
                                                 widget=forms.Select(attrs={'class':'chosen-select',
                                                                            'placeholder':'Поиск контрагента',
                                                                            'style':'height:38px',
                                                                            'tabindex':'2'}))
    DateTime_schedule   = forms.DateField(label='Запланировано на', widget=AdminDateWidget, initial=datetime.date.today)
    DateTime_work       = forms.DateField(required=False, label='Дата выполнения', widget=AdminDateWidget)
    Date_act            = forms.DateField(required=False, label='Дата акта', widget=AdminDateWidget)
    FaultAppearance     = forms.CharField(required=False, label='Неисправность', widget=forms.widgets.Textarea(attrs={'rows':3}))
    DescriptionWorks    = forms.CharField(required=False, label='Сделано', widget=forms.widgets.Textarea(attrs={'rows':3}))
    #CoWorkers           = forms.MultipleChoiceField(label='Исполнители', queryset = CoWorker.objects.filter(ServingCompany=Company,StatusWorking=True), widget=forms.widgets.SelectMultiple(attrs={'rows':5}))
    class Meta:
        model = support_request
        fields = ['NumObject','model_transmitter','num_transmitter','AddressObject','Client',
                  'FaultAppearance','DateTime_schedule','DescriptionWorks','DateTime_work','CoWorkers','Client_bd','Status','Required_act','Date_act']


class request_actrequired_fordate(forms.Form):
    request_date = forms.DateField(required=False, label='Дата', initial=datetime.datetime.today() - datetime.timedelta(days=1), widget=AdminDateWidget)