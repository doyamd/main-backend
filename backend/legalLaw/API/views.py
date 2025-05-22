from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from legalLaw.models import LegalDocument
from legalLaw.API.serializers import LegalDocumentSerializer, LegalDocumentCreateSerializer
from legalUser.API.permissions import IsAdmin
from utils.upload import upload_file

class LegalDocumentCreateView(generics.CreateAPIView):
    queryset = LegalDocument.objects.all()
    serializer_class = LegalDocumentCreateSerializer
    permission_classes = [IsAdmin]

class LegalDocumentListView(generics.ListAPIView):
    queryset = LegalDocument.objects.all()
    serializer_class = LegalDocumentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()

        categories = self.request.query_params.getlist('category')
        jurisdictions = self.request.query_params.getlist('jurisdiction')
        languages = self.request.query_params.getlist('language')
        search = self.request.query_params.get('search')

        if categories:
            queryset = queryset.filter(category__in=categories)
        if jurisdictions:
            queryset = queryset.filter(jurisdiction__in=jurisdictions)
        if languages:
            queryset = queryset.filter(language__in=languages)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset
    
class LegalDocumentByProclamationView(generics.RetrieveAPIView):
    serializer_class = LegalDocumentSerializer

    def get_queryset(self):
        return LegalDocument.objects.all()

    def get_object(self):
        proclamation_number = self.kwargs.get('proclamation_number')
        return self.get_queryset().get(proclamation_number=proclamation_number)