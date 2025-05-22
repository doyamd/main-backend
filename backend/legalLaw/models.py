from django.db import models
import uuid
from legalLaw.constants.category import LegalCategory
from legalLaw.constants.jurisdiction import Jurisdiction
from legalLaw.constants.language import Language

class LegalDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=LegalCategory.choices())
    jurisdiction = models.CharField(max_length=100, choices=Jurisdiction.choices())
    language = models.CharField(max_length=50, choices=Language.choices())
    proclamation_number = models.CharField(max_length=50)
    publication_year = models.IntegerField()
    document_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_year']
