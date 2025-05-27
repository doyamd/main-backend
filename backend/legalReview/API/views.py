# reviews/views.py
from rest_framework import generics, permissions
from legalReview.models import Review
from legalReview.API.serializers import ReviewSerializer
from legalUser.API.permissions import IsClientOrAdmin
from legalUser.models import User, Attorney
from rest_framework.exceptions import NotFound
from django.db.models import Avg

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsClientOrAdmin]

    def perform_create(self, serializer):
        serializer.save()

class AllReviewsListView(generics.ListAPIView):
    queryset = Review.objects.all().select_related('reviewer', 'attorney')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

class AttorneyReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        attorney_id = self.kwargs.get('attorney_id')
        
        try:
            attorney_user = User.objects.get(id=attorney_id, role='attorney')
        except User.DoesNotExist:
            raise NotFound("Attorney not found")

        # Get reviews for this attorney
        reviews = Review.objects.filter(attorney=attorney_user).select_related('reviewer', 'attorney')

        # Calculate average rating
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0

        # Update the related Attorney model's rating
        try:
            attorney_profile = Attorney.objects.get(user=attorney_user)
            attorney_profile.rating = round(avg_rating, 2)
            attorney_profile.save(update_fields=['rating'])
        except Attorney.DoesNotExist:
            raise NotFound("Attorney profile not found")

        return reviews