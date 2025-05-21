from django.urls import path
from legalCase.API.views import *

urlpatterns = [
    path('cases', CaseListCreateAV.as_view(), name='case-list-create'),
    path('cases/<uuid:pk>', CaseDetailAV.as_view(), name='case-detail'),
    path('case-requests', CaseRequestListCreateAV.as_view(), name='case-request-list-create'),
    path('case-requests/<uuid:pk>', CaseRequestDecisionView.as_view(), name='case-request-decision'),
]
