# analytics/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from legalUser.models import User, Attorney
from legalLaw.models import LegalDocument
from legalCase.models import CaseRequest
from legalLaw.constants.category import LegalCategory
from legalUser.constants.expertise import AttorneyExpertise
from legalUser.API.permissions import IsAdmin

class AnalyticsView(APIView):
    permission_classes = [IsAdmin]  # or a custom permission

    def get(self, request):
        users = User.objects.all()
        attorneys = Attorney.objects.all()
        
        data = {
            "total_users": users.count(),
            "attorney_users": users.filter(role="attorney").count(),
            "client_users": users.filter(role="client").count(),
            "pending_approval": attorneys.filter(is_approved=False).count(),

            "active_requests": CaseRequest.objects.filter(status="active").count(),
            "pending_requests": CaseRequest.objects.filter(status="pending").count(),
            "approved_requests": CaseRequest.objects.filter(status="approved").count(),
            "rejected_requests": CaseRequest.objects.filter(status="rejected").count(),

            "document_uploads": {
                doc_type: LegalDocument.objects.filter(category=doc_type).count()
                for doc_type in LegalCategory.values()
            },

            "case_requests": {
                case_type: CaseRequest.objects.filter(
                    attorney__attorney__expertise__contains=[case_type]
                ).count()
                for case_type in AttorneyExpertise.values()
            }
        }

        return Response(data)