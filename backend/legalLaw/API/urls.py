from django.urls import path
from legalLaw.API.views import (
    LegalDocumentCreateView,
    LegalDocumentListView,
    LegalDocumentByProclamationView,
    LegalDocumentUpdateDeleteView,
)

urlpatterns = [
    path('documents', LegalDocumentListView.as_view(), name='document-list'),
    path('documents/create', LegalDocumentCreateView.as_view(), name='document-create'),
    path('documents/proclamation/<str:proclamation_number>', LegalDocumentByProclamationView.as_view(), name='document-by-proclamation'),
    path('documents/<str:id>', LegalDocumentUpdateDeleteView.as_view(), name='document-update'),
]