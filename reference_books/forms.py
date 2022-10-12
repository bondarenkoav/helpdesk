import re

from django import forms
from accounts.views import get_scompany
from django.forms import ModelForm

from reference_books.models import ModelTransmitter, Client, CoWorker, RoutesMaintenance, SystemPCN, OpSoS_rate, \
    OpSoS_name


class addget_opsosname_form(ModelForm):
    class Meta:
        model = OpSoS_name
        fields = ['Name']


class addget_opsosrate_form(ModelForm):
    class Meta:
        model = OpSoS_rate
        fields = ['OpSoSName', 'Rate', 'price', 'Descript']


class addget_pcn_form(ModelForm):
    class Meta:
        model = SystemPCN
        fields = ['Name']


class addget_transmitter_form(ModelForm):
    class Meta:
        model = ModelTransmitter
        fields = ['Name', 'SystemPCN']


class addget_routes_form(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(addget_routes_form, self).__init__(*args, **kwargs)

        self.fields['ServiceCompany'].queryset = get_scompany(self.user)

    class Meta:
        model = RoutesMaintenance
        fields = ['ServiceCompany', 'Number', 'Descript']


class addget_client_form(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(addget_client_form, self).__init__(*args, **kwargs)

        self.fields['ServiceCompany'].queryset = get_scompany(self.user)
        self.fields['TypesClient'].widget.attrs['onchange'] = 'maskTypeClient(this)'
        self.fields['Name'].widget.attrs['id'] = 'id_Person_FIO'

    class Meta:
        model = Client
        fields = ['ServiceCompany', 'TypesClient', 'Name', 'INN', 'KPP']


class addget_coworker_form(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(addget_coworker_form, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        self.fields['ServiceCompany'].queryset = get_scompany(self.user)

    class Meta:
        model = CoWorker
        fields = ['ServiceCompany', 'Person_FIO', 'Posts', 'StatusWorking']

    def clean(self):
        cleaned_data = super(addget_coworker_form, self).clean()
        fio = re.sub(r"\s{2,}", " ", cleaned_data['Person_FIO'])

        if not self.errors:
            # Прооверка ФИО
            if re.match(r"^\w{3,}\s*\w{3,}\s*\w{5,}", fio.strip()) is None:
                raise forms.ValidationError(u'Ошибка: Фамилию имя отчество необходимо писать полностью. Сокращения не допускаются')

        return cleaned_data