# analytics/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from legalUser.models import User, Attorney
from legalLaw.models import LegalDocument
from legalCase.models import CaseRequest
from legalLaw.constants.category import LegalCategory
from legalUser.constants.expertise import AttorneyExpertise
from legalUser.API.permissions import IsAdmin

from rest_framework import status
from legalAnalytics.models import DailyAnalytics, MonthlyAnalytics, LifetimeAnalytics
from .serializers import (
    DailyAnalyticsSerializer,
    MonthlyAnalyticsSerializer,
    LifetimeAnalyticsSerializer
)
from datetime import datetime
from django.utils.dateparse import parse_date

class DailyAnalyticsView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            day = datetime.now().date()
        else:
            try:
                day = parse_date(date_str)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
        
        try:
            obj = DailyAnalytics.objects.get(date=day)
            return Response(DailyAnalyticsSerializer(obj).data)
        except DailyAnalytics.DoesNotExist:
            return Response({"error": "No analytics data for this date"}, status=404)

class MonthlyAnalyticsView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        month_str = request.query_params.get('month')
        
        if not month_str:
            # If no month provided, use current month
            current_date = datetime.now()
            month_date = current_date.replace(day=1)
        else:
            try:
                # Convert month string to integer
                month_num = int(month_str)
                if not 1 <= month_num <= 12:
                    return Response({"error": "Month must be between 1 and 12"}, status=400)
                
                # Create date with provided month and current year
                current_date = datetime.now()
                month_date = current_date.replace(month=month_num, day=1)
            except ValueError:
                return Response({"error": "Invalid month format. Use 1-12"}, status=400)
        
        try:
            obj = MonthlyAnalytics.objects.get(month=month_date)
            return Response(MonthlyAnalyticsSerializer(obj).data)
        except MonthlyAnalytics.DoesNotExist:
            return Response({"error": "No analytics data for this month"}, status=404)

class LifetimeAnalyticsView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        try:
            obj = LifetimeAnalytics.objects.get(id=1)
            return Response(LifetimeAnalyticsSerializer(obj).data)
        except LifetimeAnalytics.DoesNotExist:
            return Response({"error": "No lifetime analytics data found"}, status=404)

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