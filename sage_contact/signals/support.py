import os
from email.utils import make_msgid

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from sage_contact.models import (FullSupportRequest, SupportRequestBase,
                                 SupportRequestWithLocation,
                                 SupportRequestWithPhone)


@receiver(pre_save, sender=FullSupportRequest)
def update_contacted_before_status(sender, instance, **kwargs):
    # Check if the email has been used before in any FullSupportRequest record
    instance.contacted_before = FullSupportRequest.objects.filter(
        email=instance.email
    ).exists()


@receiver(pre_save, sender=FullSupportRequest)
def assign_user_field(sender, instance, **kwargs):
    request = kwargs.get("request", None)
    if request and request.user.is_authenticated:
        instance.user = request.user


@receiver(post_save, sender=FullSupportRequest)
def send_confirmation_email(sender, instance, created, **kwargs):
    if not created:
        return

    # Check if the SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM is True
    if not getattr(settings, "SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM", True):
        return

    # Check if the SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH is set and exists
    template_path = getattr(settings, "SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH", None)
    if not template_path or not os.path.exists(
        os.path.join(settings.BASE_DIR, template_path)
    ):
        return

    # Get the current site domain
    current_site = Site.objects.get_current()
    domain = current_site.domain

    # Create the email subject and body using an HTML template
    subject = "We have received your contact request"
    body = render_to_string(
        template_path,
        {
            "full_name": instance.full_name,
            "subject": instance.subject,
            "message": instance.message,
            "contact_reason": instance.get_contact_reason_display(),
            "preferred_contact_method": instance.get_preferred_contact_method_display(),
        },
    )

    # Create the email message
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[instance.email],
    )

    # Specify that the body is HTML
    email.content_subtype = "html"

    # Add standard headers
    email.extra_headers = {
        "MIME-Version": "1.0",
        "Content-Type": "text/html; charset=UTF-8",
        "Content-Transfer-Encoding": "quoted-printable",
        "X-Priority": "3",
        "Message-ID": make_msgid(domain=domain),
        "X-Auto-Response-Suppress": "All",
        "X-Spamd-Result": "default: False [-0.90 / 15.00]",
    }

    # Send the email
    email.send(fail_silently=False)
