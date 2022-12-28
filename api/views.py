import re
from datetime import datetime, timedelta

from django.db.migrations import serializer
from django.db.models import Q, F, Value, CharField
from django.db.models.functions import Concat
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, generics, viewsets, permissions, status
from rest_framework.viewsets import GenericViewSet

from accounts.views import get_cur_scompany, get_scompany, group_required
from api.serializers import EngineerEProposalSerializer, SupervisorEProposalSerializer, KanbanEProposalSerializer

from exploitation.models import eproposals
from reference_books.models import Status, ServiceCompanies, CoWorker, Posts


class EngineerEProposalPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


class EngineerTaskEProposalViewSet(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.ListModelMixin,
                                   GenericViewSet):
    serializer_class = EngineerEProposalSerializer
    pagination_class = EngineerEProposalPagination

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get("pk")
        if not pk:
            return eproposals.objects. \
                filter(Status__in=Status.objects.filter(slug__in=['open', 'transfer', 'control']),
                       # ServiceCompany=get_cur_scompany(user),
                       # CoWorkers__in=CoWorker.objects.filter(Posts=Posts.objects.get(slug='engineer')),
                       # CoWorkers=CoWorker.objects.get(Username=user),
                       DateTime_schedule=datetime.today()).order_by('-id')
        return eproposals.objects.filter(pk=pk)

    @action(detail=True, methods=['get'])
    def history_object(self, request, pk=None):
        obj = self.get_object()
        obj_str = re.sub(r'\s', '', obj.NumObject)
        obj_str = re.split(r'[;,\s]', obj_str)
        regex_str = r'(\s|^)%s' % obj_str[0]
        history = eproposals.objects.filter(NumObject__iregex=regex_str,
                                            DateTime_work__lte=datetime.today(),
                                            ServiceCompany=obj.ServiceCompany). \
                      annotate(Executor=F('CoWorkers__Person_FIO'),
                               Object=Concat('NumObject', Value('-'), 'AddressObject', output_field=CharField())). \
                      values('Object', 'FaultAppearance', 'DateTime_work', 'DescriptionWorks', 'Executor',
                             'DateTime_update'). \
                      order_by('-DateTime_update')[:5]
        return Response(history)


class SupervisorTaskEProposalViewSet(mixins.RetrieveModelMixin,
                                     mixins.UpdateModelMixin,
                                     mixins.ListModelMixin,
                                     GenericViewSet):
    serializer_class = SupervisorEProposalSerializer
    pagination_class = EngineerEProposalPagination

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get("pk")
        if not pk:
            return eproposals.objects. \
                filter((Q(Status=Status.objects.get(slug='open')) |
                        Q(Status=Status.objects.get(slug='transfer')) |
                        Q(Status=Status.objects.get(slug='control'))),
                       ServiceCompany=get_cur_scompany(user)).order_by('-id')
        return eproposals.objects.filter(pk=pk)


class KanbanEProposalViewSet(viewsets.ModelViewSet):
    serializer_class = KanbanEProposalSerializer

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get("pk")
        if not pk:
            return eproposals.objects.using('test'). \
                filter(Status__in=Status.objects.filter(slug__in=['open', 'complete', 'close']),
                       ServiceCompany=get_cur_scompany(user)). \
                annotate(Object=Concat('NumObject', Value('-'), 'AddressObject', output_field=CharField())). \
                order_by('-id')
        return eproposals.objects.using('test').filter(pk=pk)