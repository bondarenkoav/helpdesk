__author__ = 'ipman'

import re
from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile
from reference_books.models import ServiceCompanies, Posts
from datetime import datetime


class register_account_form(forms.Form):
    last_name = forms.CharField(label=u'Фамилия', widget=forms.TextInput())
    first_name = forms.CharField(label=u'Имя Отчество', widget=forms.TextInput())
    birthday = forms.DateField(label='Дата рождения',
                               widget=forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}), input_formats=('%Y-%m-%d', ))
    pass_new = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(),
                               help_text=u'Пароль должен состоять из цифр, букв латинского алфавита в разных регистрах.')
    pass_repeat = forms.CharField(label=u'Повтор пароля', widget=forms.PasswordInput())
    post = forms.ModelChoiceField(label=u'Должность', queryset = Posts.objects.all(), widget=forms.Select())
    scompany = forms.ModelChoiceField(label=u'Сервисная компания', queryset = ServiceCompanies.objects.all(), widget=forms.Select())
    location = forms.CharField(label=u'Место пребывания', widget=forms.TextInput())
    phone = forms.CharField(label=u'Номер телефона', widget=forms.TextInput(attrs={'step':1,'placeholder':u'в федеральном формате, без 8-ки','id':'id_phone_mobile'}))
    personal_data = forms.BooleanField(label=u'Согласие на обработку перс. данных', widget=forms.CheckboxInput())

    def clean(self):
        cleaned_data = super(register_account_form, self).clean()
        lastname = re.sub(r"\s","",cleaned_data['last_name'])
        first_name = re.sub(r"\s{2,}"," ",cleaned_data['first_name'])
        birthday = cleaned_data['birthday']
        pass_new = cleaned_data['pass_new']
        pass_repeat = cleaned_data['pass_repeat']
        phone = cleaned_data['phone']

        if not self.errors:
            # Прооверка на дубликат
            dubl = Profile.objects.filter(user__in=User.objects.filter(last_name=lastname), birthday=birthday)
            if dubl is None:
                raise forms.ValidationError(u'Пользователь с такой фамилией уже есть в системе.')

            # Прооверка ФИО
            if re.match(r"\D{3,}", lastname.strip()) == None:
                raise forms.ValidationError(u'Ошибка: Фамилия не может быть менее трёх букв')

            result = re.split(r" ", first_name, maxsplit=1)
            if len(result)==2:
                if re.match(r"\D{3,}", result[0]) == None:
                    raise forms.ValidationError(u'Ошибка: Имя не может быть менее трёх букв')

                if re.match(r"\D{5,}", result[1]) == None:
                    raise forms.ValidationError(u'Ошибка: Отчество не может быть менее пяти букв')
            else:
                raise forms.ValidationError(u'Ошибка: Введите имя и отчество')

            # Возраст
            calculate_age = datetime.today().year - birthday.year - ((datetime.today().month, datetime.today().day) < (birthday.month, birthday.day))
            if calculate_age < 18:
                raise forms.ValidationError(u'Вы слишком молоды чтобы работать у нас')

            # Пароли
            if pass_new != pass_repeat:
                raise forms.ValidationError(u'Пароли не совпадают')
            else:
                if bool(re.match("((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8})", pass_new)) == False:
                    raise forms.ValidationError(u'Пароль недостаточно сложен')

        return cleaned_data


class forgot_password_form(forms.Form):
    username = forms.CharField(label=u'Логин', widget=forms.TextInput())
    birthday = forms.DateField(label='Дата рождения',
                               widget=forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}), input_formats=('%Y-%m-%d', ))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'id':'id_phone_mobile'}),
                            help_text=u'Номер в федеральном формате (без 8 или +7')

    def clean(self):
        cleaned_data = super(forgot_password_form, self).clean()
        username = cleaned_data['username']
        birthday = cleaned_data['birthday']

        if not self.errors:
            user = Profile.objects.get(user=User.objects.get(username=username), birthday=birthday)
            if user is None:
                raise forms.ValidationError(u'Имя пользователя и дата рождения не подходят')
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user or None


class update_profile_form(forms.Form):
    birthday = forms.DateField(label='Дата рождения',
                               widget=forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}),
                               input_formats=('%Y-%m-%d', ))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'id':'id_phone_mobile'}),
                            help_text=u'Номер в федеральном формате (без 8 или +7')

    def clean(self):
        cleaned_data = super(update_profile_form, self).clean()
        birthday = cleaned_data['birthday']

        if not self.errors:
            # Возраст
            calculate_age = datetime.today().year - birthday.year - ((datetime.today().month, datetime.today().day) < (birthday.month, birthday.day))
            if calculate_age < 18:
                raise forms.ValidationError(u'Вы слишком молоды чтобы работать у нас')

        return cleaned_data


class change_password_form(forms.Form):
    username = forms.CharField(required=False, widget=forms.HiddenInput())
    pass_hidden = forms.CharField(required=False, widget=forms.HiddenInput())
    pass_sms = forms.CharField(label=u'Пароль из СМС', widget=forms.TextInput())
    pass_new = forms.CharField(label=u'Пароль новый', widget=forms.PasswordInput(),
                               help_text=u'Пароль должен состоять из цифр, букв латинского алфавита в разных регистрах.')
    pass_repeat = forms.CharField(label=u'Повтор пароля', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(change_password_form, self).clean()
        username = cleaned_data['username']
        pass_hidden = cleaned_data['pass_hidden']
        try:
            pass_sms = cleaned_data['pass_sms']
            pass_new = cleaned_data['pass_new']
            pass_repeat = cleaned_data['pass_repeat']

            if not self.errors:
                if pass_hidden == pass_sms:
                    if pass_new == pass_repeat:
                        if bool(re.match("((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8})", pass_new)) is False:
                            raise forms.ValidationError(u'Новый пароль не достаточно сложен')
                    else:
                        raise forms.ValidationError(u'Новый пароль и повторный пароль не одинаковы')
                else:
                    raise forms.ValidationError(u'Введенный Вами пароль из СМС-сообщения не верен')
                self.username = username
                self.pass_new = pass_new
        except:
            pass
        return cleaned_data


class change_cur_scompany_form(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(change_cur_scompany_form, self).__init__(*args, **kwargs)
        profile = Profile.objects.get(user=self.user)

        self.fields['cur_scompany'].queryset = profile.scompany
        if profile.scompany_current:
            self.fields['cur_scompany'].initial = profile.scompany_current
        elif profile.scompany_default:
            self.fields['cur_scompany'].initial = profile.scompany_default
        else:
            self.fields['cur_scompany'].initial = profile.scompany.all().first()

    cur_scompany = forms.ModelChoiceField(label=u'Сервисная компания',
                                          queryset=Profile.objects.values('scompany').all(),
                                          initial=Profile.scompany_current,
                                          widget=forms.Select(attrs={'class': 'custom-select'}))
