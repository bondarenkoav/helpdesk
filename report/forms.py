import datetime
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

__author__ = 'ipman'

# class coworkers_object(forms.Form):          # Вывести: кто монтировал объект и сколько
#
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super(coworkers_object, self).__init__(*args, **kwargs)
#
#         type_id     = TypeRequest.objects.get(slug='build').id
#         status_id   = Status.objects.get(slug='complete').id
#         Company     = ExpandedUserProfile.objects.get(UserName=self.user).ServingCompany
#
#         self.fields['build_request'].queryset = support_request.objects.filter(Status=status_id,Company=Company)
#         self.fields['build_request'].widget.attrs['class'] = 'selector'
#
#     #type_id     = TypeRequest.objects.get(slug='build').id
#     #status_id   = Status.objects.get(slug='complete').id
#     #request_num = forms.ModelChoiceField(required=False, label='Заявка на монтаж', help_text="Выберите заявку на монтаж со статусом ИСПОЛНЕНО", queryset = support_request.objects.filter(TypeRequest=type_id,Status=status_id), widget=forms.Select(attrs={'class':'selector'}))
#     class Meta:
#         model = acts_build
#         fields = ['build_request']
#
# class coworker_range_date(forms.Form):          # Вывести: где работал один исполнитель за период
#
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super(coworker_range_date, self).__init__(*args, **kwargs)
#
#         Company = ExpandedUserProfile.objects.get(UserName=self.user).ServingCompany
#
#         self.fields['CoWorkers'].queryset = CoWorker.objects.filter(ServingCompany=Company)
#         self.fields['CoWorkers'].widget.attrs['class'] = 'selector'
#
#     CoWorkers       = forms.ModelChoiceField(queryset=None, empty_label=None)
#     acts_date_start = forms.DateField(label='Дата начала', widget=SelectDateWidget, initial=datetime.date.today)
#     acts_date_stop  = forms.DateField(label='Дата окончания', widget=SelectDateWidget, initial=datetime.date.today)
#     no_range_date   = forms.BooleanField(label='За весь период', required=False, widget=CheckboxInput)
#     class Meta:
#         model = CoWorker
#         fields = ['CoWorkers']

KIND_CHOICES = (
    ('by_date', u'по дате'),
    ('by_cowork', u'по исполнителю'),
)


class coworkers_range_date(forms.Form):          # Вывести: кто где работал в течении заданного периода и за один день
    kind = forms.ChoiceField(required=True, label="Статус", choices=KIND_CHOICES,
                             widget=forms.Select(attrs={'class':'selector'}))
    acts_date_start = forms.DateField(required=True, label='Дата начала', initial=datetime.datetime.today(),
                                      widget=forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}), input_formats=('%Y-%m-%d', ))
    acts_date_stop  = forms.DateField(required=False, label='Дата окончания', help_text='Указываем последний день обслуживания',
                                      widget=forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}), input_formats=('%Y-%m-%d', ))
