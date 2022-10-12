from datetime import datetime, timedelta
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import modelformset_factory

from accounts.models import Profile
from reference_books.models import Status_task, TypeNotification_task, TypeSecurity, MaterialsWorks, AdditionallyWorks, \
    SetMaterials, Status_calc
from tasks.models import user_task, Calculations, CalcMaterialsWorks


class form_calc_operator(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(form_calc_operator, self).__init__(*args, **kwargs)

        self.fields['Description'].label = u'Дополнительная информация'

    ContactPerson = forms.CharField(label=u'ФИО контактного лица',
                                    widget=forms.widgets.TextInput(attrs={'id': 'id_Person_FIO'}))
    TypeTask = forms.ModelMultipleChoiceField(label=u'Тип сигнализации',
                                              widget=forms.CheckboxSelectMultiple(attrs={'style': 'margin-left: .75rem;'}),
                                              queryset=TypeSecurity.objects.all().order_by('id'))
    Phone = forms.CharField(label=u'Номер телефона', widget=forms.widgets.TextInput(attrs={'id': 'id_phone_mobile'}))

    class Meta:
        model = Calculations
        fields = ['ContactPerson', 'TypeTask', 'Description', 'AddressObject', 'NameObject', 'Phone', 'Address_email']


# Делегирование задачи
class form_calc_disposer(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(form_calc_disposer, self).__init__(*args, **kwargs)

        group = Group.objects.get(name='executor')
        users = group.user_set.all()
        list_profiles = Profile.objects.filter(user__in=users.filter(is_active=True))
        self.fields['executor'].queryset = list_profiles

    class Meta:
        model = Calculations
        fields = ['executor']


# Делегирование задачи
class form_calc_executor(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super(form_calc_executor, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        #self.fields['client_consent'].required = False

        if instance.DateTime_inspection_object:
            self.fields['Date_inspection'].initial = datetime.date(instance.DateTime_inspection_object)
            self.fields['Time_inspection'].initial = datetime.time(instance.DateTime_inspection_object+timedelta(hours=5))

        if self.profile == instance.executor:
            if instance.DateTime_inspection_object is None:
                self.fields['Date_inspection'].required = True
                self.fields['Time_inspection'].required = True
                self.fields['Channels_connection'].required = False
                self.fields['Channels_connection'].widget.attrs['disabled'] = 'disabled'
                self.fields['Frequency_tests'].required = False
                self.fields['Frequency_tests'].widget.attrs['disabled'] = 'disabled'
                self.fields['Estimate'].required = False
                self.fields['Estimate'].widget.attrs['disabled'] = 'disabled'

            self.fields['Date_waiting'].required = False
            self.fields['Date_waiting'].widget.attrs['disabled'] = 'disabled'
            self.fields['Date_actual'].required = False
            self.fields['Date_actual'].widget.attrs['disabled'] = 'disabled'
            self.fields['Date_build'].required = False
            self.fields['Date_build'].widget.attrs['disabled'] = 'disabled'
            self.fields['Workorder'].required = False
            self.fields['Workorder'].widget.attrs['disabled'] = 'disabled'

            if instance.total_summ == 0 and instance.Estimate:
                self.fields['Estimate'].label = 'Скан сметы'

        else:
            self.fields['ContactPerson'].required = False
            self.fields['ContactPerson'].widget.attrs['disabled'] = 'disabled'
            self.fields['TypeTask'].required = False
            self.fields['TypeTask'].widget.attrs['disabled'] = 'disabled'
            self.fields['Description'].required = False
            self.fields['Description'].widget.attrs['disabled'] = 'disabled'
            self.fields['AddressObject'].required = False
            self.fields['AddressObject'].widget.attrs['disabled'] = 'disabled'
            self.fields['NameObject'].required = False
            self.fields['NameObject'].widget.attrs['disabled'] = 'disabled'
            self.fields['Phone'].required = False
            self.fields['Phone'].widget.attrs['disabled'] = 'disabled'
            self.fields['Address_email'].required = False
            self.fields['Address_email'].widget.attrs['disabled'] = 'disabled'
            self.fields['Channels_connection'].required = False
            self.fields['Channels_connection'].widget.attrs['disabled'] = 'disabled'
            self.fields['Frequency_tests'].required = False
            self.fields['Frequency_tests'].widget.attrs['disabled'] = 'disabled'
            self.fields['Estimate'].required = False
            self.fields['Estimate'].widget.attrs['disabled'] = 'disabled'
            self.fields['Date_waiting'].required = False
            self.fields['Date_waiting'].widget.attrs['disabled'] = 'disabled'
            self.fields['Date_actual'].required = False
            self.fields['Date_actual'].widget.attrs['disabled'] = 'disabled'
            self.fields['Date_build'].required = False
            self.fields['Date_build'].widget.attrs['disabled'] = 'disabled'
            self.fields['Workorder'].required = False
            self.fields['Workorder'].widget.attrs['disabled'] = 'disabled'

    ContactPerson = forms.CharField(label=u'ФИО контактного лица',
                                    widget=forms.widgets.TextInput(attrs={'id': 'id_Person_FIO'}))
    Phone = forms.CharField(label=u'Номер сим-карты', widget=forms.widgets.TextInput(attrs={'id': 'id_phone_mobile'}))
    TypeTask = forms.ModelMultipleChoiceField(label=u'Тип сигнализации',
                                              widget=forms.CheckboxSelectMultiple(attrs={'style': 'margin-left: .75rem;'}),
                                              queryset=TypeSecurity.objects.all().order_by('id'))
    Description = forms.CharField(required=False, label=u'Описание', widget=forms.Textarea(attrs={'rows': '5'}))
    Date_inspection = forms.DateField(label=u'Дата осмотра объекта', input_formats=('%Y-%m-%d',),
                                      widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    Time_inspection = forms.TimeField(label=u'Время осмотра объекта', input_formats=('%H:%M',),
                                      widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    Status = forms.ModelChoiceField(required=False, label=u'Статус',
                                    queryset=Status_calc.objects.all().order_by('id'),
                                    widget=forms.Select())

    class Meta:
        model = Calculations
        fields = ['ContactPerson', 'TypeTask', 'Description', 'AddressObject', 'NameObject', 'Phone', 'Address_email',
                  'Channels_connection', 'Frequency_tests',
                  'Estimate', 'Date_waiting', 'Date_actual',
                  'Date_build', 'Workorder', 'Act_Delivery', 'client_consent', 'Status']


class form_calc_additional_fields(forms.ModelForm):

    commissioning = forms.ModelChoiceField(required=False, label=u'Пусконаладочные работы',
                                           queryset=AdditionallyWorks.objects.filter(type='commissioning').order_by('id'),
                                           widget=forms.Select())
    projects = forms.ModelChoiceField(required=False, label=u'Проектные работы',
                                      queryset=AdditionallyWorks.objects.filter(type='projects').order_by('id'),
                                      widget=forms.Select())
    Sale = forms.IntegerField(label=u'Снижение стоимости работ, %', min_value=0, max_value=25,
                              widget=forms.NumberInput(attrs={'onchange': 'CalcNewTotalSumm();', 'id': 'id_sale'}))

    class Meta:
        model = Calculations
        fields = ['commissioning', 'projects', 'Sale']


class form_add_task(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(form_add_task, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        self.fields['executor'].required = False
        self.fields['group_executor'].queryset = Group.objects.filter(name__in=['Администрация Орск', 'Администрация Оренбург'])
        self.fields['executor'].queryset = Profile.objects.\
            filter(user__in=User.objects.
                   filter(groups__in=Group.objects.filter(name__in=['accountants', 'governance', 'managers']), is_active=True).
                   order_by('last_name')).order_by('user__last_name')
        self.fields['read'].required = False
        self.fields['read'].widget.attrs['disabled'] = 'disabled'

        if instance and instance.id:
            if instance.group_executor:
                self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['status'].initial = Status_task.objects.get(slug='open', view_list=True)
            self.fields['status'].required = False
            self.fields['status'].widget.attrs['disabled'] = 'disabled'

        # if instance and instance.id:
        #     if self.user != instance.author:
        #         self.fields['title'].required = False
        #         self.fields['title'].widget.attrs['disabled'] = 'disabled'
        #         self.fields['description'].required = False
        #         self.fields['description'].widget.attrs['disabled'] = 'disabled'
        #         self.fields['executor'].required = False
        #         self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        #         self.fields['Date_limit'].required = False
        #         self.fields['Date_limit'].widget.attrs['disabled'] = 'disabled'
        #         self.fields['high_importance'].required = False
        #         self.fields['high_importance'].widget.attrs['disabled'] = 'disabled'
        #         self.fields['notification'].required = False
        #         self.fields['notification'].widget.attrs['disabled'] = 'disabled'
        #         self.fields['status'].queryset = Status_task.objects.filter(view_list=True).exclude(slug__in=['canceled',])
        #     else:
        #         self.fields['status'].queryset = Status_task.objects.filter(view_list=True)
        #
        #     if self.group_executor:
        #         self.fields['executor'].required = False
        #         self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        # else:
        #     self.fields['executor'].required = False
        #     self.fields['notification'].inintial = TypeNotification_task.objects.get(slug='system')
        #     self.fields['status'].initial = Status_task.objects.get(slug='open', view_list=True)
        #     self.fields['status'].required = False
        #     self.fields['status'].widget.attrs['disabled'] = 'disabled'
        #     self.fields['work_desc'].required = False
        #     self.fields['work_desc'].widget.attrs['disabled'] = 'disabled'
        #     self.fields['status'].queryset = Status_task.objects.filter(view_list=True)
        #
        # list_users = User.objects.\
        #     filter(groups__in=Group.objects.exclude(name__in=['engineers', 'operators']), is_active=True).\
        #     order_by('last_name')
        # self.fields['group_executor'].queryset = Group.objects.filter(name__in=['Администрация Орск', 'Администрация Оренбург'])
        # self.fields['executor'].queryset = Profile.objects.filter(user__in=list_users).order_by('user__last_name')
        # self.fields['read'].required = False
        # self.fields['read'].widget.attrs['disabled'] = 'disabled'

    Date_limit = forms.DateField(input_formats=('%Y-%m-%d',), initial=datetime.today(),
                                 widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    description = forms.CharField(required=False, label='Описание задачи',
                                  widget=forms.widgets.Textarea(attrs={'rows': 3}))
    work_desc = forms.CharField(required=False, label='Описание выполнения',
                                widget=forms.widgets.Textarea(attrs={'rows': 3}))

    class Meta:
        model = user_task
        fields = ['title', 'description', 'executor', 'group_executor', 'Date_limit', 'client',
                  'high_importance', 'notification', 'status', 'work_desc', 'read', 'file']


class form_fill_materials(forms.Form):

    set = forms.ModelChoiceField(required=True, label=u'Набор',
                                 queryset=SetMaterials.objects.all(), widget=forms.Select())


class form_calculations(forms.ModelForm):

    material = forms.ModelChoiceField(required=False, label=u'Материал', queryset=MaterialsWorks.objects.all(),
                                      widget=forms.Select())
    quantity = forms.IntegerField(required=False, label=u'Кол-во', min_value=0)
    material_rent = forms.BooleanField(required=False, label='')

    class Meta:
        model = CalcMaterialsWorks
        fields = ['material', 'quantity', 'material_rent']


MaterialsFormSet = modelformset_factory(CalcMaterialsWorks, form=form_calculations, extra=1)
