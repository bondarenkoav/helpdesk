from django import forms
from django.forms import ModelForm
from maintenance.models import objects_to
from reference_books.models import ModelTransmitter, Client, CoWorker, RoutesMaintenance

__author__ = 'ipman'


class get_new_save_transmitter(ModelForm):
    class Meta:
        model = ModelTransmitter
        fields = ['Name','SystemPCN']

class get_add_routes(ModelForm):
    class Meta:
        model = RoutesMaintenance
        fields = ['Number','Descript']

class get_new_save_client(ModelForm):

    def __init__(self, *args, **kwargs):
        super(get_new_save_client, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['Name'].required = False
            self.fields['Name'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Client
        fields = ['Name']

class co_worker_form(ModelForm):
    class Meta:
        model = CoWorker
        fields = ['Person_FIO','Posts','StatusWorking']