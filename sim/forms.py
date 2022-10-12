import os

from django.core.exceptions import ValidationError

__author__ = 'ipman'

from sim.models import OpSoS_card
from django import forms
from django.forms import ModelForm, Form
from reference_books.models import SystemPCN
from accounts.views import get_cur_scompany, get_scompany


class get_new_simcard(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(get_new_simcard, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        Company = get_scompany(self.user)
        Company_cur = get_cur_scompany(self.user)

        if instance and instance.id:
            self.fields['Number_SIM'].widget.attrs['id'] = ''
            self.fields['Number_SIM'].required = False
            self.fields['Number_SIM'].widget.attrs['disabled'] = 'disabled'
            self.fields['ServiceCompany'].required = False
            self.fields['ServiceCompany'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['Use_type'].initial = 'usesim_none'
            self.fields['ServiceCompany'].queryset = Company
            self.fields['ServiceCompany'].initial = Company_cur.id

        self.fields['Use_type'].widget.attrs['onchange'] = 'hideInputTypeUseSIM(this)'

    Number_SIM = forms.CharField(label=u'Номер сим-карты',
                                 widget=forms.widgets.TextInput(attrs={'id': 'id_phone_mobile'}))
    ICC_SIM = forms.CharField(label=u'ID сим-карты', widget=forms.widgets.TextInput())
    Contract_date = forms.DateField(required=True, label='Дата заключения', input_formats=('%Y-%m-%d',),
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    Notation = forms.CharField(required=False, label='Примечание', widget=forms.widgets.Textarea(attrs={'rows': 3}))
    SystemPCN = forms.ModelChoiceField(required=True, label='Тип использования', queryset=SystemPCN.objects.all(),
                                       help_text='Выберите тип применения и заполните доступное поле/поля ниже',
                                       widget=forms.Select())
    Use_numberobject = forms.CharField(required=False, label='№ объекта', widget=forms.widgets.TextInput())
    Use_nameobject = forms.CharField(required=False, label='Наименование объекта', widget=forms.widgets.TextInput())
    Use_addressobject = forms.CharField(required=False, label='Адрес объекта',
                                        widget=forms.widgets.TextInput(attrs={'id': 'id_AddressObject'}))
    Use_user = forms.CharField(required=False, label='ФИО пользователя',
                               widget=forms.widgets.TextInput(attrs={'id': 'id_Person_FIO'}))

    class Meta:
        model = OpSoS_card
        fields = ['OpSoSRate', 'Number_SIM', 'ICC_SIM', 'SystemPCN', 'Contract', 'ServiceCompany', 'Contract_date',
                  'PersonalAccount', 'Status', 'archive',
                  'Use_type', 'Use_numberobject', 'Use_nameobject', 'Use_addressobject', 'Use_user', 'Notation']

    def clean(self):
        cleaned_data = super(get_new_simcard, self).clean()
        icc_sim = cleaned_data['ICC_SIM']
        #usetype = cleaned_data.get('Use_type')
        #useuser = cleaned_data['Use_user']
        # usenumobject = cleaned_data['Use_numberobject'].replace('', '')
        # usenameobject = cleaned_data['Use_nameobject'].replace(' ', '')
        # useaddressobject = cleaned_data['Use_addressobject'].replace(' ', '')

        if not self.errors:
            if self.instance.id is None:
                if icc_sim.isdigit() is False:
                    raise forms.ValidationError(u'Идентификационный код сим-карты состоит только из цифр')
                # if usetype == 'usesim_user':
                #    if useuser.isalpha() == False:
                #        raise forms.ValidationError(u'Поле ФИО должно содержать только буквы')
                # elif usetype == 'usesim_object':
                #    if usenumobject.isalnum() == False or usenameobject.isalnum() == False:
                #        raise forms.ValidationError(u'Поля данных по объекту не должны содержать спецсимволы')
        return cleaned_data
