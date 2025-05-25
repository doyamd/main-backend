# analytics/utils.py
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from legalUser.models import User, Attorney
from legalLaw.models import LegalDocument
from legalCase.models import CaseRequest
from legalLaw.constants.category import LegalCategory
from legalUser.constants.expertise import AttorneyExpertise
from legalAnalytics.models import DailyAnalytics, MonthlyAnalytics, LifetimeAnalytics
from datetime import date, timedelta

def populate_analytics():
    today = now().date() - timedelta(days=30)
    first_day_of_month = today.replace(day=1)

    users = User.objects.all()
    attorneys = Attorney.objects.all()

    analytics_data = {
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

    DailyAnalytics.objects.update_or_create(
        date=today,
        defaults=analytics_data
    )

    MonthlyAnalytics.objects.update_or_create(
        month=first_day_of_month,
        defaults=analytics_data
    )

    LifetimeAnalytics.objects.update_or_create(
        id=1,
        defaults=analytics_data
    )

def _get_analytics_records():
    today = now().date()
    month = today.replace(day=1)

    daily, _ = DailyAnalytics.objects.get_or_create(date=today)
    monthly, _ = MonthlyAnalytics.objects.get_or_create(month=month)
    lifetime, _ = LifetimeAnalytics.objects.get_or_create(id=1)
    
    return daily, monthly, lifetime

def update_analytics(event_type, **kwargs):
    daily, monthly, lifetime = _get_analytics_records()

    # Central map
    def increment(field, amount=1):
        for obj in [daily, monthly, lifetime]:
            setattr(obj, field, getattr(obj, field, 0) + amount)

    if event_type == "user_signup":
        role = kwargs.get("role")
        increment("total_users")
        if role == "attorney":
            increment("attorney_users")
        elif role == "client":
            increment("client_users")

    elif event_type == "case_request":
        case_type = kwargs.get("case_type")
        status = kwargs.get("status")
        increment("case_requests__" + case_type)
        if status:
            if status == "pending":
                increment("pending_requests")
            elif status == "active":
                increment("active_requests")
            elif status == "approved":
                increment("approved_requests")
            elif status == "rejected":
                increment("rejected_requests")

    elif event_type == "case_status_update":
        from_status = kwargs.get("from_status")
        to_status = kwargs.get("to_status")
        if from_status:
            if from_status == "pending":
                increment("pending_requests", -1)
            elif from_status == "active":
                increment("active_requests", -1)
            elif from_status == "approved":
                increment("approved_requests", -1)
            elif from_status == "rejected":
                increment("rejected_requests", -1)
        if to_status:
            if to_status == "pending":
                increment("pending_requests", 1)
            elif to_status == "active":
                increment("active_requests", 1)
            elif to_status == "approved":
                increment("approved_requests", 1)
            elif to_status == "rejected":
                increment("rejected_requests", 1)

    elif event_type == "document_upload":
        doc_type = kwargs.get("document_type")
        for obj in [daily, monthly, lifetime]:
            uploads = obj.document_uploads
            uploads[doc_type] = uploads.get(doc_type, 0) + 1
            obj.document_uploads = uploads

    for obj in [daily, monthly, lifetime]:
        obj.save()