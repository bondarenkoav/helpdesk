from api.views import *

from django.urls import path, include, re_path
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'engineer-task', EngineerTaskEProposalViewSet, basename='engineer')
router.register(r'supervisor', SupervisorTaskEProposalViewSet, basename='supervisor')

urlpatterns = [
    # path('tasks/', KanbanListTask.as_view()),
    path('', include(router.urls)),
]