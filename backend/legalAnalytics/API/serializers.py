# analytics/serializers.py
from rest_framework import serializers
from legalAnalytics.models import DailyAnalytics, MonthlyAnalytics, LifetimeAnalytics

class BaseAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class DailyAnalyticsSerializer(BaseAnalyticsSerializer):
    class Meta(BaseAnalyticsSerializer.Meta):
        model = DailyAnalytics

class MonthlyAnalyticsSerializer(BaseAnalyticsSerializer):
    class Meta(BaseAnalyticsSerializer.Meta):
        model = MonthlyAnalytics

class LifetimeAnalyticsSerializer(BaseAnalyticsSerializer):
    class Meta(BaseAnalyticsSerializer.Meta):
        model = LifetimeAnalytics