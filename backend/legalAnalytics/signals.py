from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from legalCase.models import CaseRequest
from legalLaw.models import LegalDocument
from legalUser.models import User, Attorney
from utils.analytics import update_analytics


# ---- USER SIGNUP SIGNAL ----
@receiver(post_save, sender=User)
def handle_user_signup(sender, instance, created, **kwargs):
    if created:
        user_type = getattr(instance, "role", None)
        if user_type in ["client", "attorney"]:
            update_analytics("user_signup", role=user_type)

# ---- CASE REQUEST CREATED SIGNAL ----
@receiver(post_save, sender=CaseRequest)
def handle_case_request(sender, instance, created, **kwargs):
    if created:
        try:
            # Get the attorney instance linked to the User
            attorney = Attorney.objects.get(user=instance.attorney)
            expertise_list = attorney.expertise or []

            for expertise in expertise_list:
                update_analytics("case_request", case_type=expertise, status=instance.status)
        except Attorney.DoesNotExist:
            pass  

# ---- CASE REQUEST STATUS CHANGE SIGNAL ----
@receiver(pre_save, sender=CaseRequest)
def track_case_status_change(sender, instance, **kwargs):
    try:
        old = sender.objects.get(pk=instance.pk)
        if old.status != instance.status:
            update_analytics("case_status_update", from_status=old.status, to_status=instance.status)
    except sender.DoesNotExist:
        pass  # New instance, no previous status

# ---- DOCUMENT UPLOAD SIGNAL ----
@receiver(post_save, sender=LegalDocument)
def handle_document_upload(sender, instance, created, **kwargs):
    if created:
        update_analytics("document_upload", document_type=instance.category)