# check.py
import os

from django.conf import settings
from django.core.checks import Error, register
from django.template.utils import get_app_template_dirs


@register()
def check_geoip_path(app_configs, **kwargs):
    errors = []
    geoip_path = getattr(settings, "GEOIP_PATH", None)

    if geoip_path is not None and not os.path.exists(geoip_path):
        errors.append(
            Error(
                "GEOIP_PATH is set to a non-existent path",
                hint="Ensure the path set in GEOIP_PATH exists.",
                id="geoip.E002",
            )
        )

    # Check for SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH
    send_email = getattr(settings, "SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM", True)
    template_path = getattr(settings, "SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH", None)

    if send_email:
        if not template_path:
            errors.append(
                Error(
                    "SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH is not set",
                    hint="Set the SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH in settings.",
                    id="sage_contact.E001",
                )
            )
        else:
            # Check in BASE_DIR first
            if not os.path.exists(os.path.join(settings.BASE_DIR, template_path)):
                # If not found in BASE_DIR, check in app template directories
                template_found = False
                for template_dir in get_app_template_dirs("templates"):
                    if os.path.exists(os.path.join(template_dir, template_path)):
                        template_found = True
                        break
                if not template_found:
                    errors.append(
                        Error(
                            "SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH is set to a non-existent path",
                            hint="Ensure the path set in SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH exists.",
                            id="sage_contact.E002",
                        )
                    )

    # Additional check for email settings when DEBUG is False
    if not settings.DEBUG and send_email:
        if not getattr(settings, "EMAIL_HOST", None):
            errors.append(
                Error(
                    "EMAIL_HOST is not set",
                    hint=(
                        "The EMAIL_HOST must be set in settings because DEBUG is False and "
                        "SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM is True. Ensure all necessary "
                        "email settings are configured for the application to send emails in "
                        "production."
                    ),
                    id="sage_contact.E001",
                )
            )
        if not getattr(settings, "EMAIL_PORT", None):
            errors.append(
                Error(
                    "EMAIL_PORT is not set",
                    hint=(
                        "The EMAIL_PORT must be set in settings because DEBUG is False and "
                        "SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM is True. Ensure all necessary "
                        "email settings are configured for the application to send emails in "
                        "production."
                    ),
                    id="sage_contact.E002",
                )
            )
        if not getattr(settings, "EMAIL_HOST_USER", None):
            errors.append(
                Error(
                    "EMAIL_HOST_USER is not set",
                    hint=(
                        "The EMAIL_HOST_USER must be set in settings because DEBUG is False and "
                        "SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM is True. Ensure all necessary "
                        "email settings are configured for the application to send emails in "
                        "production."
                    ),
                    id="sage_contact.E003",
                )
            )
        if not getattr(settings, "EMAIL_HOST_PASSWORD", None):
            errors.append(
                Error(
                    "EMAIL_HOST_PASSWORD is not set",
                    hint=(
                        "The EMAIL_HOST_PASSWORD must be set in settings because DEBUG is False and "
                        "SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM is True. Ensure all necessary "
                        "email settings are configured for the application to send emails in "
                        "production."
                    ),
                    id="sage_contact.E004",
                )
            )
        if not getattr(settings, "EMAIL_USE_TLS", None):
            errors.append(
                Error(
                    "EMAIL_USE_TLS is not set",
                    hint=(
                        "The EMAIL_USE_TLS must be set in settings because DEBUG is False and "
                        "SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM is True. Ensure all necessary "
                        "email settings are configured for the application to send emails in "
                        "production."
                    ),
                    id="sage_contact.E005",
                )
            )

    return errors
