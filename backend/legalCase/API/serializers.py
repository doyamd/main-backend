from rest_framework import serializers
from legalCase.models import Case

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'document', 'is_probono', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_available', 'created_at', 'updated_at', 'document']