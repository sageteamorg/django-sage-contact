from django.conf import settings
from django.core.validators import (EmailValidator, MaxLengthValidator,
                                    MinLengthValidator, RegexValidator)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicManager, PolymorphicModel
from sage_tools.mixins.models.base import TimeStampMixin

from sage_contact.constants.choices import ContactMethods, ContactReasons


class SupportRequestBase(TimeStampMixin, PolymorphicModel):
    subject = models.CharField(
        _("Subject"),
        max_length=100,
        help_text=_("The main topic of your message."),
        db_comment="The subject of the contact message.",
        validators=[
            MinLengthValidator(1, message=_("The subject cannot be empty.")),
            MaxLengthValidator(
                100, message=_("The subject must be 100 characters or fewer.")
            ),
        ],
    )

    full_name = models.CharField(
        _("Full Name"),
        max_length=100,
        help_text=_("Your complete name as you'd like us to address you."),
        db_comment="The full name of the person contacting.",
        validators=[
            MinLengthValidator(1, message=_("The full name cannot be empty.")),
            MaxLengthValidator(
                100, message=_("The full name must be 100 characters or fewer.")
            ),
            RegexValidator(
                r"^[a-zA-Z]+([ \'\-][a-zA-Z]+)*$",
                _(
                    "Enter a valid name. The name can only contain letters, spaces, hyphens, and apostrophes. Examples: John Doe, Mary-Jane O'Connor."
                ),
            ),
        ],
    )

    email = models.EmailField(
        _("Email"),
        max_length=254,
        help_text=_("Your email address where we can send a reply."),
        db_comment="The email address of the person contacting.",
        validators=[
            EmailValidator(message=_("Enter a valid email address.")),
            MaxLengthValidator(
                254, message=_("The email must be 254 characters or fewer.")
            ),
        ],
    )

    message = models.TextField(
        _("Message"),
        help_text=_("The detailed message or inquiry you wish to submit."),
        db_comment="The contact message content.",
        validators=[MinLengthValidator(1, message=_("The message cannot be empty."))],
    )

    objects = PolymorphicManager()

    class Meta:
        verbose_name = _("Basic Contact")
        verbose_name_plural = _("Basic Contacts")
        default_manager_name = "objects"
        db_table = "sage_support_base"
        db_table_comment = "Table to store basic contact information including subject, full name, email, and message."

    def __str__(self):
        return f"{self.full_name}"

    def __repr__(self):
        return f"<SupportRequestBase {self.full_name}>"


class SupportRequestWithPhone(SupportRequestBase):
    phone_number = PhoneNumberField(
        _("Phone Number"),
        help_text=_("Your phone number in international format, e.g., +12025550109."),
        db_comment="The international phone number of the person contacting.",
    )

    class Meta:
        verbose_name = _("Contact With Phone")
        verbose_name_plural = _("Contacts With Phone")
        db_table = "sage_support_with_phone"
        db_table_comment = "Table to store contact information including phone number along with basic contact details."


class SupportRequestWithLocation(SupportRequestWithPhone):
    country = CountryField(
        _("Country"),
        blank_label="(select country)",
        help_text=_(
            "Select the country you are contacting us from. Useful for regional marketing campaigns and statistics."
        ),
        db_comment="The country of the person contacting.",
    )

    ip_address = models.GenericIPAddressField(
        _("IP Address"),
        unpack_ipv4=True,
        blank=True,
        null=True,
        help_text=_(
            "For internal use only. Your IP address is recorded for security and demographic purposes."
        ),
        db_comment="The IP address from which the contact form was submitted.",
    )

    class Meta:
        verbose_name = _("Contact With Location")
        verbose_name_plural = _("Contacts With Location")
        db_table = "sage_support_with_location"
        db_table_comment = "Table to store contact information including location details along with phone and basic contact details."


class FullSupportRequest(SupportRequestWithLocation):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            "If you are a registered user, this field links your account to the contact form."
        ),
        db_comment="A reference to the User model if the contact is made by a registered user.",
    )

    contacted_before = models.BooleanField(
        _("Contacted Before"),
        default=False,
        help_text=_(
            "Check this box if you have made previous contact. It helps us track our ongoing relationship with you."
        ),
        db_comment="Indicates whether the person has contacted the company before.",
    )

    contact_reason = models.CharField(
        _("Reason for Contact"),
        max_length=200,
        choices=ContactReasons.choices,
        help_text=_(
            "Specify the reason for your contact. This helps us to direct your query to the appropriate team."
        ),
        db_comment="The reason for the contact, used to categorize and prioritize the contact.",
    )

    preferred_contact_method = models.CharField(
        _("Preferred Contact Method"),
        max_length=50,
        choices=ContactMethods.choices,
        help_text=_(
            "Indicate your preferred method of communication. We respect your choice and will contact you accordingly."
        ),
        db_comment="The contact's preferred method of communication.",
    )

    class Meta:
        verbose_name = _("Full Contact")
        verbose_name_plural = _("Full Contacts")
        db_table = "sage_full_support"
        db_table_comment = "Table to store complete contact information including user reference, contact history, reason for contact, preferred contact method, and all details from location, phone, and basic contact."
