# analytics/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("realtime", AnalyticsView.as_view(), name="realtime-analytics"),
    path("daily", DailyAnalyticsView.as_view(), name="daily-analytics"),
    path("monthly", MonthlyAnalyticsView.as_view(), name="monthly-analytics"),
    path("lifetime", LifetimeAnalyticsView.as_view(), name="lifetime-analytics")
]