from django.db import migrations
import random
from datetime import datetime, timedelta

def generate_random_reviews(apps, schema_editor):
    User = apps.get_model('legalUser', 'User')
    Review = apps.get_model('legalReview', 'Review')

    # Get all clients and attorneys
    clients = User.objects.filter(role='client')
    attorneys = User.objects.filter(role='attorney')

    # Sample review texts
    review_texts = [
        "Great attorney, very professional and knowledgeable.",
        "Excellent service, would recommend to others.",
        "Very helpful and responsive throughout the case.",
        "Good experience working with this attorney.",
        "Professional and thorough in their approach.",
        "Very satisfied with the legal services provided.",
        "Excellent communication and expertise.",
        "Highly recommended for legal matters.",
        "Very knowledgeable in their field.",
        "Great attention to detail and client care.",
        "Professional and efficient service.",
        "Very helpful in explaining legal matters.",
        "Excellent representation and guidance.",
        "Very satisfied with the outcome.",
        "Great experience working with this attorney."
    ]

    # Create reviews
    for client in clients:
        # Each client reviews 1-3 random attorneys
        for attorney in random.sample(list(attorneys), k=random.randint(1, min(3, len(attorneys)))):
            Review.objects.create(
                reviewer=client,
                attorney=attorney,
                rating=random.randint(1, 5),
                review_text=random.choice(review_texts) if random.random() > 0.2 else "",  # 20% chance of no review text
                created_at=datetime.now() - timedelta(days=random.randint(1, 365))  # Random date within last year
            )

def reverse_func(apps, schema_editor):
    Review = apps.get_model('legalReview', 'Review')
    Review.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('legalReview', '0001_initial'),
        ('legalUser', '0002_add_random_data'),  # Make sure this runs after the user data is created
    ]

    operations = [
        migrations.RunPython(generate_random_reviews, reverse_func),
    ] 