import datetime

from rest_framework import serializers

from accounts.models import Profile
from exploitation.models import eproposals
from reference_books.models import Status, CoWorker


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('Name',)


class CoworkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoWorker
        fields = ('Person_FIO', 'Username',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'scompany', 'scompany_current')


class EngineerEProposalSerializer(serializers.ModelSerializer):
    NumObject = serializers.CharField(read_only=True)
    AddressObject = serializers.CharField(read_only=True)
    Client_words = serializers.CharField(read_only=True)
    FaultAppearance = serializers.CharField(read_only=True)
    DateTime_schedule = serializers.DateField(read_only=True)
    DateTime_work = serializers.DateField(read_only=True)
    CoWorkers = CoworkersSerializer(many=True, read_only=True)
    Required_act = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        if instance.is_valid():
            instance.Status = Status.objects.get(slug='complete')
            instance.DateTime_work = datetime.datetime.now().date()
        instance.save()
        return instance

    class Meta:
        model = eproposals
        fields = ('id', 'NumObject', 'AddressObject', 'Client_words', 'FaultAppearance', 'DescriptionWorks',
                  'DateTime_schedule', 'DateTime_work', 'Status', 'CoWorkers', 'Required_act', 'Written_act')


class SupervisorEProposalSerializer(serializers.ModelSerializer):
    NumObject = serializers.CharField(read_only=True)
    AddressObject = serializers.CharField(read_only=True)
    Client_words = serializers.CharField(read_only=True)
    FaultAppearance = serializers.CharField(read_only=True)
    DateTime_schedule = serializers.DateField()
    Status = StatusSerializer(many=False)
    CoWorkers = CoworkersSerializer(many=True)
    Required_act = serializers.BooleanField(read_only=True)
    Written_act = serializers.BooleanField(read_only=True)
    Date_act = serializers.DateField(read_only=True)
    DescriptionWorks = serializers.DateField(read_only=True)
    DateTime_add = serializers.DateTimeField(read_only=True)
    DateTime_update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = eproposals
        fields = ('id', 'NumObject', 'AddressObject', 'Client_words', 'FaultAppearance', 'DescriptionWorks',
                  'DateTime_schedule', 'DateTime_work', 'Status', 'CoWorkers', 'Required_act', 'Written_act',
                  'Date_act', 'DateTime_add', 'DateTime_update', 'Create_user', 'Update_user')


class KanbanEProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = eproposals
        fields = ('id', 'NumObject', 'AddressObject', 'Client_words', 'FaultAppearance', 'DescriptionWorks',
                  'DateTime_schedule', 'DateTime_work', 'Status')
        read_only_fields = ('NumObject', 'AddressObject', 'Client_words', 'FaultAppearance')

    def update(self, instance, validated_data):
        boardName = self.initial_data.get('boardName')
        date_schedule = None
        currdate = datetime.datetime.now().date()
        if instance.Status.Name == 'Принята' and boardName not in ['Завершено', 'Исполнено']:
            if boardName == 'Сегодня':
                date_schedule = currdate
            elif boardName == 'Завтра':
                date_schedule = currdate + datetime.timedelta(days=1)
            elif boardName == 'Понедельник':
                delta = 7 - currdate.isoweekday() + 1
                date_schedule = currdate + datetime.timedelta(days=delta)
        validated_data.update({'DateTime_schedule': date_schedule})

        return super().update(instance, validated_data)


