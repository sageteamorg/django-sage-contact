from django.db.models.signals import pre_save
from django.dispatch import receiver

from sage_contact.models import FullSupportRequest


@receiver(pre_save, sender=FullSupportRequest)
def update_contacted_before_status(sender, instance, **kwargs):
    # Check if the email has been used before in any FullSupportRequest record
    instance.contacted_before = FullSupportRequest.objects.filter(
        email=instance.email
    ).exists()

@receiver(pre_save, sender=FullSupportRequest)
def assign_user_field(sender, instance, **kwargs):
    request = kwargs.get('request', None)
    if request and request.user.is_authenticated:
        instance.user = request.user
