from django.urls import path
from legalCase.API.views import *

urlpatterns = [
    path('cases', CaseListCreateAV.as_view(), name='case-list-create'),
    path('cases/<uuid:pk>', CaseDetailAV.as_view(), name='case-detail'),
]
