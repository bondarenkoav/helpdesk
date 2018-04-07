from datetime import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import CheckboxInput
from reference_books import models
from reference_books.models import CoWorker, ExpandedUserProfile

__author__ = 'ipman'

from django.contrib.auth import authenticate
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label=u'Логин')
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

# type_request = {
#     'trouble': 'Эксплуатация',
#     'build': 'Монтаж',
#     'maintenance': 'Техническое обслуживание',
# }
type_request = (
    ('trouble', u'Эксплуатация'),
    ('build', u'Монтаж'),
    ('maintenance', u'Техническое обслуживание')
)

class search_form(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super(search_form, self).__init__(*args, **kwargs)
    #     Company = ExpandedUserProfile.objects.get(UserName=self.user).ServingCompany

        # self.fields['coworkers'].label = u'Исполнитель'
        # self.fields['coworkers'].widget = forms.Select(attrs={'class':'selector'})
        # self.fields['coworkers'].queryset = CoWorker.objects.filter(ServingCompany=Company,StatusWorking=True)

    requestdate   = forms.DateField(label=u'Дата', initial=datetime.today, widget=AdminDateWidget)
    norangedate   = forms.BooleanField(label=u'За весь период', required=False, widget=CheckboxInput)
    typerequest   = forms.ChoiceField(label=u'Тип заявки', choices=type_request, widget=forms.Select, required=False)
    coworkers     = forms.ModelChoiceField(label=u'Исполнитель', required=False, queryset=models.CoWorker.objects.all(), widget=forms.Select(attrs={'class':'selector'}))
    status        = forms.ModelChoiceField(label=u'Состояние', required=False, queryset=models.Status.objects.all(), widget=forms.Select(attrs={'class':'selector'}))
    numobject     = forms.CharField(label=u'Номер объекта', required=False, widget=forms.widgets.NumberInput)

    def clean(self):
        cleaned_data = super(search_form, self).clean()
        norangedate = cleaned_data['norangedate']
        requestdate = cleaned_data['requestdate']

        if norangedate != True:
            if requestdate is None:
                self._errors['requestdate'] = self.error_class([u'Введите дату поиска'])

        return cleaned_data