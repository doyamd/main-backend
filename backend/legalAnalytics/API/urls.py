# analytics/urls.py
from django.urls import path
from .views import AnalyticsView

urlpatterns = [
    path("realtime", AnalyticsView.as_view(), name="realtime-analytics"),
]