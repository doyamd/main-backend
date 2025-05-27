from rest_framework import serializers
from legalCase.models import Case, CaseRequest
from legalUser.models import User, Attorney
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
    
class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class CaseMiniSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)

    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'document', 'user', 'is_probono', 'is_available']

class AttorneyWithCaseStatsSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    cases = serializers.SerializerMethodField()

    class Meta:
        model = Attorney
        fields = ['id', 'user', 'bio', 'starting_price', 'is_available', 'offers_probono',
                  'address', 'rating', 'profile_completion', 'license_document', 'is_approved', 'expertise', 'cases']

    def get_cases(self, obj):
        # Get all case requests for this attorney
        case_requests = CaseRequest.objects.filter(attorney=obj.user)

        # Count by status
        pending_count = case_requests.filter(status='pending').count()
        accepted_count = case_requests.filter(status='accepted').count()
        declined_count = case_requests.filter(status='declined').count()

        # Get the actual Case objects for accepted case requests
        accepted_case_ids = case_requests.filter(status='accepted').values_list('case_id', flat=True)
        accepted_cases = Case.objects.filter(id__in=accepted_case_ids)

        return {
            'pending': pending_count,
            'accepted': accepted_count,
            'declined': declined_count,
            'accepted_data': CaseSerializer(accepted_cases, many=True).data
        }


class CaseWithUserSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'document', 'is_probono', 'is_available', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'is_available', 'created_at', 'updated_at', 'document']
