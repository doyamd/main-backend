import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from legalUser.constants.expertise import AttorneyExpertise

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=255, choices=[('client', 'Client'), ('attorney', 'Attorney'), ('admin', 'Admin')])
    password = models.CharField(max_length=255)
    image = models.TextField(max_length=150, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
class OTP(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    otp = models.CharField(max_length=6, )
    user = models.OneToOneField(User, related_name="otp_user", on_delete=models.CASCADE)
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_probono = models.BooleanField(default=False)
    probono_document = models.TextField(max_length=255, null=True, blank=True)
    probono_approved_at = models.DateTimeField(null=True, blank=True)
    probono_expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.email
    
class Attorney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    starting_price = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=False)
    offers_probono = models.BooleanField(default=False)
    address = models.TextField(max_length=255)
    rating = models.FloatField(default=0)
    profile_completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    license_document = models.TextField(max_length=255)
    is_approved = models.BooleanField(default=False)
    expertise = models.CharField(
        max_length=50,
        choices=AttorneyExpertise.choices(),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.email
    
class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attorney = models.ForeignKey(Attorney, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return self.institution
    
class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attorney = models.ForeignKey(Attorney, on_delete=models.CASCADE)
    organization = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    years = models.IntegerField()

    def __str__(self):
        return self.organization
    

class AttorneyEducation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attorney = models.ForeignKey(Attorney, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attorney.user.email} - {self.education.institution}"
    
class AttorneyExperience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attorney = models.ForeignKey(Attorney, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attorney.user.email} - {self.experience.organization}"