from django.urls import path
from legalReview.API.views import ReviewCreateView, AllReviewsListView, AttorneyReviewsView

urlpatterns = [
    path('', AllReviewsListView.as_view(), name='review-list'),
    path('create', ReviewCreateView.as_view(), name='review-create'),
    path('<uuid:attorney_id>', AttorneyReviewsView.as_view(), name='attorney-reviews'),
]