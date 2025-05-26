from django.db import migrations
import random
import uuid
from datetime import datetime, timedelta
from legalUser.constants.expertise import AttorneyExpertise

def generate_random_data(apps, schema_editor):
    User = apps.get_model('legalUser', 'User')
    OTP = apps.get_model('legalUser', 'OTP')
    Client = apps.get_model('legalUser', 'Client')
    Attorney = apps.get_model('legalUser', 'Attorney')
    Education = apps.get_model('legalUser', 'Education')
    Experience = apps.get_model('legalUser', 'Experience')
    Case = apps.get_model('legalCase', 'Case')
    CaseRequest = apps.get_model('legalCase', 'CaseRequest')

    # Create admin user
    admin_user = User.objects.create(
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        role="admin",
        password="bcrypt_sha256$$2b$12$31WZTrM7OP.kHo/u4ukIa.v/D0PYV9gvj7p4Je8JqECVwXo9Wevou"  # In real app, this should be properly hashed
    )

    # Create some attorneys
    attorney_users = []
    for i in range(5):
        user = User.objects.create(
            first_name=f"Attorney{i+1}",
            last_name=f"Lawyer{i+1}",
            email=f"attorney{i+1}@example.com",
            role="attorney",
            password="bcrypt_sha256$$2b$12$31WZTrM7OP.kHo/u4ukIa.v/D0PYV9gvj7p4Je8JqECVwXo9Wevou"
        )
        attorney_users.append(user)
        
        attorney = Attorney.objects.create(
            user=user,
            bio=f"Experienced attorney specializing in various legal matters. Attorney {i+1}",
            starting_price=random.uniform(100, 500),
            is_available=random.choice([True, False]),
            offers_probono=random.choice([True, False]),
            address=f"{random.randint(100, 999)} Main St, City{i+1}",
            rating=random.uniform(3.0, 5.0),
            profile_completion=random.randint(70, 100),
            license_document="license_doc_url",
            is_approved=True,
            expertise=random.sample(list(AttorneyExpertise.values()), k=random.randint(1, 3))
        )

        # Add education for each attorney
        for _ in range(random.randint(1, 3)):
            Education.objects.create(
                attorney=attorney,
                institution=f"University of Law {random.randint(1, 5)}",
                degree=random.choice(["JD", "LLM", "BA in Law"]),
                year=random.randint(2000, 2020)
            )

        # Add experience for each attorney
        for _ in range(random.randint(1, 4)):
            Experience.objects.create(
                attorney=attorney,
                organization=f"Law Firm {random.randint(1, 10)}",
                title=random.choice(["Associate", "Partner", "Senior Attorney"]),
                years=random.randint(1, 15)
            )

    # Create some clients
    client_users = []
    for i in range(10):
        user = User.objects.create(
            first_name=f"Client{i+1}",
            last_name=f"Person{i+1}",
            email=f"client{i+1}@example.com",
            role="client",
            password="bcrypt_sha256$$2b$12$31WZTrM7OP.kHo/u4ukIa.v/D0PYV9gvj7p4Je8JqECVwXo9Wevou"
        )
        client_users.append(user)
        
        Client.objects.create(
            user=user,
            is_probono=random.choice([True, False]),
            probono_status=random.choice(['not_applied', 'pending', 'approved', 'rejected']),
            probono_document="probono_doc_url" if random.choice([True, False]) else None,
            probono_approved_at=datetime.now() if random.choice([True, False]) else None,
            probono_expires_at=datetime.now() + timedelta(days=365) if random.choice([True, False]) else None
        )

    # Create some cases
    for i in range(15):
        case = Case.objects.create(
            user=random.choice(client_users),
            title=f"Legal Case {i+1}",
            description=f"Description for legal case {i+1}. This is a detailed description of the legal matter.",
            document="case_document_url",
            is_probono=random.choice([True, False]),
            is_available=random.choice([True, False])
        )

        # Create case requests
        for _ in range(random.randint(1, 3)):
            CaseRequest.objects.create(
                case=case,
                attorney=random.choice(attorney_users),
                status=random.choice(['pending', 'accepted', 'declined']),
                response_message="Interested in taking this case" if random.choice([True, False]) else None,
                responded_at=datetime.now() if random.choice([True, False]) else None
            )

    # Create some OTPs
    for user in User.objects.all():
        OTP.objects.create(
            user=user,
            otp=str(random.randint(100000, 999999)),
            expired_at=datetime.now() + timedelta(minutes=10)
        )

def reverse_func(apps, schema_editor):
    User = apps.get_model('legalUser', 'User')
    User.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('legalUser', '0001_initial'),
        ('legalCase', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_random_data, reverse_func),
    ] 