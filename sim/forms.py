from time import strptime
from sim.models import OpSoS_card, UseTypeSIM

__author__ = 'ipman'

import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from django.forms import ModelForm, SplitDateTimeWidget, CheckboxInput, modelformset_factory


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

    Number_SIM          = forms.CharField(required=False, label=u'Номер сим-карты', widget=forms.widgets.TextInput(attrs={'id':'phone_mobile'}))
    ICC_SIM             = forms.CharField(required=False, label=u'ID сим-карты', widget=forms.widgets.TextInput(attrs={'id':'id_sim'}))
    Contract_date       = forms.DateField(label='Дата заключения', widget=AdminDateWidget, initial=datetime.date.today)
    Notation            = forms.CharField(required=False, label='Примечание', widget=forms.widgets.Textarea(attrs={'rows':3}))
    Use_type            = forms.ModelChoiceField(required=True, label='Тип использования', queryset = UseTypeSIM.objects.all(),
                                                 help_text='Выберите тип применения и заполните доступное поле/поля ниже',
                                                 widget=forms.Select(attrs={'class':'selector','onchange':'hideInputTypeUseSIM(this)'}))
    Use_numberobject    = forms.CharField(required=False, label='№ объекта', widget=forms.widgets.TextInput(attrs={'disabled':'disabled'}))
    Use_nameobject      = forms.CharField(required=False, label='Наименование объекта', widget=forms.widgets.TextInput(attrs={'disabled':'disabled'}))
    Use_addressobject   = forms.CharField(required=False, label='Адрес объекта', widget=forms.widgets.TextInput(attrs={'disabled':'disabled'}))
    Use_user            = forms.CharField(required=False, label='ФИО пользователя', widget=forms.widgets.TextInput(attrs={'disabled':'disabled'}))

    class Meta:
        model = OpSoS_card
        fields = ['OpSoSRate','Number_SIM','ICC_SIM','SystemPCN','Contract','Owner','Contract_date','PersonalAccount','Status',
                  'Use_type','Use_numberobject','Use_nameobject','Use_addressobject','Use_user']

    # def clean(self):
    #     cleaned_data = super(get_new_simcard, self).clean()
    #     full_name = cleaned_data['full_name']
    #     passport_sernum = cleaned_data['passport_sernum']
    #
    #     if full_name and passport_sernum:
    #         if re.match(r"^[А-Яа-я]{3,}\s[А-Яа-я]{3,}\s[А-Яа-я]{3,}",full_name) == None:
    #             raise forms.ValidationError(u'Ошибка: ФИО должно быть полным')
    #
    #         # Проверка паспортных данных
    #         if re.match(r"^([0-9]{4})\s{1}([0-9]{6})$",passport_sernum) == None:
    #             raise forms.ValidationError(u'Введите серию и номер паспорта в формате ХХХХ ХХХХХХ')
    #
    #         if not self.errors:
    #             self.full_name = full_name
    #             self.passport_sernum = passport_sernum
    #
    #             client = Branch.objects.filter(Client__in=Client.objects.filter(NameClient_full=full_name,PassportSerNum=passport_sernum))
    #             if client:
    #                 if client.count() > 1:
    #                     raise forms.ValidationError(u'В базе данных обнаружен дубликат контрагента')
    #                 self.client = Branch.objects.get(Client=Client.objects.get(NameClient_full=full_name,PassportSerNum=passport_sernum))
    #             else:
    #                 self.client = None
    #         return cleaned_data