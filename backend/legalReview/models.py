from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from legalUser.models import User
import uuid

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews',
        help_text="Client who is giving the review"
    )

    attorney = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        help_text="Attorney being reviewed"
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 (worst) to 5 (best)"
    )

    review_text = models.TextField(
        max_length=1000,
        blank=True,
        help_text="Optional written feedback"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'attorney')  # one review per client per attorney

    def __str__(self):
        return f"{self.reviewer.email} → {self.attorney.email} ({self.rating})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.reviewer.role != 'client':
            raise ValidationError("Only clients can submit reviews.")
        if self.attorney.role != 'attorney':
            raise ValidationError("Only attorneys can be reviewed.")