from rest_framework import serializers
from legalCase.models import Case, CaseRequest
from datetime import timezone, datetime

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'document', 'is_probono', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_available', 'created_at', 'updated_at', 'document']


class CaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseRequest
        fields = ['id', 'case', 'attorney', 'status', 'response_message', 'requested_at', 'responded_at']
        read_only_fields = ['status', 'response_message', 'requested_at', 'responded_at']

    def validate(self, data):
        case = data.get('case')
        attorney = data.get('attorney')

        # Prevent duplicate request
        if CaseRequest.objects.filter(case=case, attorney=attorney).exists():
            raise serializers.ValidationError("This attorney has already been requested for this case.")

        return data
    
class CaseRequestDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseRequest
        fields = ['id', 'status', 'response_message']

    def validate_status(self, value):
        if value not in ['accepted', 'declined']:
            raise serializers.ValidationError("Status must be either 'accepted' or 'declined'")
        return value

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.response_message = validated_data.get('response_message', instance.response_message)
        now = datetime.now(tz=timezone.utc)
        instance.responded_at = now
        instance.save()
        return instance