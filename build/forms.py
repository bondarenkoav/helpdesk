import datetime
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, CheckboxInput
from django.forms.extras import SelectDateWidget
from build.models import acts_build, build_request
from claim.models import TypeRequest, support_request
from reference_books.models import ExpandedUserProfile, CoWorker, Status, Client

__author__ = 'ipman'

now_date = datetime.date.today()
cur_month = now_date.month
cur_year = now_date.year

class get_new_save_request(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(get_new_save_request, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         self.fields['TypeRequest'].required = False
    #         self.fields['TypeRequest'].widget.attrs['disabled'] = 'disabled'
    #         self.fields['AddressObject'].required = False
    #         self.fields['AddressObject'].widget.attrs['disabled'] = 'disabled'
    #         self.fields['Client'].queryset = Client.objects.all()

    Client = forms.ModelChoiceField(required=False, label='Контрагент', queryset = Client.objects.all(), widget=forms.Select(attrs={'class':'chosen-select', 'placeholder':'Поиск контрагента', 'style':'height:38px', 'tabindex':'2'}))
    #Client = forms.ModelChoiceField(required=False, label='Контрагент', queryset = Client.objects.all(), widget=Select2Widget)
    DateTime_schedule = forms.DateTimeField(label='Запланировано на', widget=AdminDateWidget, initial=datetime.date.today)
    DateTime_work = forms.DateTimeField(required=False, label='Дата выполнения', widget=AdminDateWidget)
    DescriptionWorks = forms.CharField(required=False, label='Описание', widget=forms.widgets.Textarea(attrs={'rows':3}))
    class Meta:
        model = build_request
        fields = ['TypeRequest','Client','AddressObject','TypeSecurity','DateTime_schedule','DescriptionWorks','DateTime_work','model_transmitter','num_transmitter','Status']

class get_new_save_acts_build(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(get_new_save_acts_build, self).__init__(*args, **kwargs)
        Company = ExpandedUserProfile.objects.get(UserName=self.user).ServingCompany
        self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServingCompany=Company)
        self.fields['CoWorkers'].widget.attrs['size'] = '20'

    Day_reporting   = forms.DateField(required=True, label='Отчетная дата', widget=AdminDateWidget, initial=datetime.date.today)
    Description = forms.CharField(required=False, label='Описание', widget=forms.widgets.Textarea(attrs={'rows':5}))
    class Meta:
        model = acts_build
        fields = ['Day_reporting', 'CoWorkers', 'Description']

class coworkers_range_date(forms.Form):          # Вывести: кто где работал в течении заданного периода и за один день
    acts_date_start = forms.DateField(label='Дата начала', widget=AdminDateWidget, initial=datetime.date.today)
    acts_date_stop  = forms.DateField(label='Дата окончания', widget=AdminDateWidget, initial=datetime.date.today)

class coworkers_object(forms.Form):          # Вывести: кто монтировал объект и сколько

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(coworkers_object, self).__init__(*args, **kwargs)

        type_id     = TypeRequest.objects.get(slug='build').id
        status_id   = Status.objects.get(slug='complete').id
        Company     = ExpandedUserProfile.objects.get(UserName=self.user).ServingCompany

        self.fields['build_request'].queryset = support_request.objects.filter(Status=status_id,Company=Company)
        self.fields['build_request'].widget.attrs['class'] = 'selector'

    #type_id     = TypeRequest.objects.get(slug='build').id
    #status_id   = Status.objects.get(slug='complete').id
    #request_num = forms.ModelChoiceField(required=False, label='Заявка на монтаж', help_text="Выберите заявку на монтаж со статусом ИСПОЛНЕНО", queryset = support_request.objects.filter(TypeRequest=type_id,Status=status_id), widget=forms.Select(attrs={'class':'selector'}))
    class Meta:
        model = acts_build
        fields = ['build_request']

class coworker_range_date(forms.Form):          # Вывести: где работал один исполнитель за период

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(coworker_range_date, self).__init__(*args, **kwargs)

        Company = ExpandedUserProfile.objects.get(UserName=self.user).ServingCompany

        self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServingCompany=Company)
        self.fields['CoWorkers'].widget.attrs['class'] = 'selector'

    CoWorkers       = forms.ModelChoiceField(queryset=None, empty_label=None)
    acts_date_start = forms.DateField(label='Дата начала', widget=AdminDateWidget, initial=datetime.date.today)
    acts_date_stop  = forms.DateField(label='Дата окончания', widget=AdminDateWidget, initial=datetime.date.today)
    no_range_date   = forms.BooleanField(label='За весь период', required=False, widget=CheckboxInput)
    class Meta:
        model = CoWorker
        fields = ['CoWorkers']