from api.views import *

from django.urls import path, include, re_path
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'engineer', EngineerTaskEProposalViewSet, basename='engineer')
router.register(r'supervisor', SupervisorTaskEProposalViewSet, basename='supervisor')
router.register(r'kanban', KanbanEProposalViewSet, basename='kanban')
print(router.urls)

urlpatterns = [
    path('', include(router.urls)),
]