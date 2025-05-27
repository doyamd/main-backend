# reviews/serializers.py
from rest_framework import serializers
from legalReview.models import Review
from legalUser.models import User, Attorney
from django.db.models import Avg

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserBasicSerializer(read_only=True)
    attorney = UserBasicSerializer(read_only=True)

    attorney_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'attorney', 'attorney_id', 'rating', 'review_text', 'created_at']
        read_only_fields = ['id', 'reviewer', 'attorney', 'created_at']

    def validate_attorney_id(self, value):
        try:
            user = User.objects.get(id=value)
            if user.role != 'attorney':
                raise serializers.ValidationError("You can only review attorneys.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Attorney not found.")
        return value

    def create(self, validated_data):
        request = self.context['request']
        reviewer = request.user
        attorney_user = User.objects.get(id=validated_data.pop('attorney_id'))

        # Create the review
        review = Review.objects.create(reviewer=reviewer, attorney=attorney_user, **validated_data)

        # Update attorney's average rating
        avg_rating = Review.objects.filter(attorney=attorney_user).aggregate(avg=Avg('rating'))['avg'] or 0.0

        # Update the Attorney model's rating field
        try:
            attorney_profile = Attorney.objects.get(user=attorney_user)
            attorney_profile.rating = round(avg_rating, 2)
            attorney_profile.save()
        except Attorney.DoesNotExist:
            pass  # You can raise an exception or log this if needed

        return review