# analytics/models.py
from django.db import models
from django.utils import timezone

class BaseAnalytics(models.Model):
    total_users = models.PositiveIntegerField(default=0)
    attorney_users = models.PositiveIntegerField(default=0)
    client_users = models.PositiveIntegerField(default=0)

    pending_approval = models.PositiveIntegerField(default=0)

    active_requests = models.PositiveIntegerField(default=0)
    pending_requests = models.PositiveIntegerField(default=0)
    approved_requests = models.PositiveIntegerField(default=0)
    rejected_requests = models.PositiveIntegerField(default=0)

    document_uploads = models.JSONField(default=dict)
    case_requests = models.JSONField(default=dict)

    class Meta:
        abstract = True

class DailyAnalytics(BaseAnalytics):
    date = models.DateField(unique=True)

class MonthlyAnalytics(BaseAnalytics):
    month = models.DateField(unique=True)  

class LifetimeAnalytics(BaseAnalytics):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    last_updated = models.DateTimeField(auto_now=True)