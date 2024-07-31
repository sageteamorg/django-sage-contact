from django.conf import settings
from django.core.validators import EmailValidator, MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from sage_contact.constants.choices import Prefix


class Label(models.Model):
    """
    Model representing a label used to organize contacts into groups.
    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
        null=False,
        help_text=_("Unique name for the label"),
        db_comment="Unique name for the label",
    )

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")
        db_table = "sage_label"
        db_table_comment = "Labels help in organizing contacts into groups."

    def __str__(self):
        return f"{self.name}"


class Contact(models.Model):
    """
    Model representing a contact with various personal and professional details.
    """

    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=255,
        null=False,
        help_text=_("Contact's first name"),
        db_comment="Contact's first name",
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=255,
        null=False,
        help_text=_("Contact's last name"),
        db_comment="Contact's last name",
    )
    middle_name = models.CharField(
        verbose_name=_("Middle Name"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Contact's middle name"),
        db_comment="Contact's middle name",
    )
    nickname = models.CharField(
        verbose_name=_("Nickname"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Contact's nickname"),
        db_comment="Contact's nickname",
    )
    prefix = models.CharField(
        verbose_name=_("Prefix"),
        max_length=3,
        choices=Prefix.choices,
        null=True,
        blank=True,
        help_text=_("Contact's name prefix (e.g., Mr., Mrs., Dr.)"),
        db_comment="Contact's name prefix (e.g., Mr., Mrs., Dr.)",
    )
    suffix = models.CharField(
        verbose_name=_("Suffix"),
        max_length=50,
        null=True,
        blank=True,
        help_text=_("Contact's name suffix (e.g., Jr., Sr., III)"),
        db_comment="Contact's name suffix (e.g., Jr., Sr., III)",
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=255,
        null=True,
        blank=True,
        validators=[
            EmailValidator(message=_("Enter a valid email address.")),
            MaxLengthValidator(
                254, message=_("The email must be 254 characters or fewer.")
            ),
        ],
        help_text=_("Contact's email address"),
        db_comment="Contact's email address",
    )
    phone_number = PhoneNumberField(
        _("Phone Number"),
        null=True,
        blank=True,
        help_text=_("Contact's phone number"),
        db_comment="Contact's phone number",
    )
    physical_address = models.TextField(
        verbose_name=_("Physical Address"),
        null=True,
        blank=True,
        help_text=_("Contact's physical address"),
        db_comment="Contact's physical address",
    )
    im_handle = models.CharField(
        verbose_name=_("IM Handle"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Instant messaging handle (e.g., Skype, Slack)"),
        db_comment="Instant messaging handle (e.g., Skype, Slack)",
    )
    website = models.URLField(
        verbose_name=_("Website"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Contact's website URL"),
        db_comment="Contact's website URL",
    )
    company = models.CharField(
        verbose_name=_("Company"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Company where the contact works"),
        db_comment="Company where the contact works",
    )
    job_title = models.CharField(
        verbose_name=_("Job Title"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Job title of the contact"),
        db_comment="Job title of the contact",
    )
    department = models.CharField(
        verbose_name=_("Department"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Department of the contact"),
        db_comment="Department of the contact",
    )
    birthday = models.DateField(
        verbose_name=_("Birthday"),
        null=True,
        blank=True,
        help_text=_("Contact's birthday"),
        db_comment="Contact's birthday",
    )
    anniversary = models.DateField(
        verbose_name=_("Anniversary"),
        null=True,
        blank=True,
        help_text=_("Contact's anniversary date"),
        db_comment="Contact's anniversary date",
    )
    notes = models.TextField(
        verbose_name=_("Notes"),
        null=True,
        blank=True,
        help_text=_("Additional notes about the contact"),
        db_comment="Additional notes about the contact",
    )
    photo = models.URLField(
        verbose_name=_("Photo"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("URL or path to the contact's photo"),
        db_comment="URL or path to the contact's photo",
    )

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        db_table = "sage_contact"
        db_table_comment = "Table to store contact details similar to Google Contacts."


class CustomField(models.Model):
    """
    Model representing a custom field for a contact to store additional user-defined information.
    """

    contact = models.ForeignKey(
        to=Contact,
        on_delete=models.CASCADE,
        help_text=_("Foreign key to Contact table"),
        db_comment="Foreign key to Contact",
    )
    field_name = models.CharField(
        max_length=255,
        help_text=_("Name of the custom field"),
        db_comment="Custom field name",
    )
    field_value = models.CharField(
        max_length=255,
        help_text=_("Value of the custom field"),
        db_comment="Custom field value",
    )

    class Meta:
        verbose_name = _("Custom Field")
        verbose_name_plural = _("Custom Fields")
        db_table = "sage_customfield"
        db_table_comment = (
            "Custom fields allow additional user-defined information for each contact."
        )

    def __str__(self):
        return f"{self.field_name}: {self.field_value}"


class ContactLabel(models.Model):
    """
    Model representing the many-to-many relationship between contacts and labels.
    """

    contact = models.ForeignKey(
        to=Contact,
        on_delete=models.CASCADE,
        help_text=_("Foreign key to Contact table"),
        db_comment="Foreign key to Contact",
    )
    label = models.ForeignKey(
        to=Label,
        on_delete=models.CASCADE,
        help_text=_("Foreign key to Label table"),
        db_comment="Foreign key to Label",
    )

    class Meta:
        unique_together = ["contact", "label"]
        verbose_name = _("Contact Label")
        verbose_name_plural = _("Contact Labels")
        db_table = "sage_contactlabel"
        db_table_comment = (
            "Table to manage the many-to-many relationship between contacts and labels."
        )

    def __str__(self):
        return f"{self.contact} - {self.label}"
