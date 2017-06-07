from time import strptime
from sim.models import OpSoS_card, UseTypeSIM

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


class get_new_simcard(ModelForm):
    def __init__(self, *args, **kwargs):
        super(get_new_simcard, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            data = OpSoS_card.objects.get(id=instance.id)
            self.fields['OpSoSRate'].required = False
            self.fields['OpSoSRate'].widget.attrs['disabled'] = 'disabled'
            self.fields['Number_SIM'].required = False
            self.fields['Number_SIM'].widget.attrs['disabled'] = 'disabled'
            self.fields['ICC_SIM'].required = False
            self.fields['ICC_SIM'].widget.attrs['disabled'] = 'disabled'
            self.fields['Owner'].required = False
            self.fields['Owner'].widget.attrs['disabled'] = 'disabled'
            self.fields['PersonalAccount'].required = False
            self.fields['PersonalAccount'].widget.attrs['disabled'] = 'disabled'
            self.fields['Contract'].required = False
            self.fields['Contract'].widget.attrs['disabled'] = 'disabled'
            self.fields['Contract_date'].required = False
            self.fields['Contract_date'].widget.attrs['disabled'] = 'disabled'
            if data.Status == False:
                self.fields['Status'].required = False
                self.fields['Status'].widget.attrs['disabled'] = 'disabled'
        else:
            pass

    Contract_date       = forms.DateField(label='Дата заключения', widget=AdminDateWidget, initial=datetime.date.today)
    Notation            = forms.CharField(required=False, label='Примечание', widget=forms.widgets.Textarea(attrs={'rows':3}))
    Use_type            = forms.ModelChoiceField(required=True, label='Тип использования', queryset = UseTypeSIM.objects.all(), help_text='Выберите тип применения и заполните доступное поле/поля ниже', widget=forms.Select(attrs={'class':'selector','onchange':'hideInputTypeUseSIM(this)'}))
    Use_numberobject    = forms.CharField(required=False, label='№ объекта', widget=forms.widgets.TextInput(attrs={'disabled':'disabled'}))
    Use_addressobject   = forms.CharField(required=False, label='Адрес объекта', widget=forms.widgets.TextInput(attrs={'disabled':'disabled'}))
    Use_user            = forms.CharField(required=False, label='ФИО пользователя', widget=forms.widgets.TextInput(attrs={'disabled':'disabled'}))
    class Meta:
        model = OpSoS_card
        fields = ['OpSoSRate','Number_SIM','ICC_SIM','Contract','Owner','Contract_date','PersonalAccount','Status','Use_type','Use_numberobject','Use_addressobject','Use_user']