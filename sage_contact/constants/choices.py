from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactReasons(models.TextChoices):
    """
    Content Reasons
    """

    SUPPORT = ("support", _("Support"))
    SALES = ("sales", _("Sales Inquiry"))
    FEEDBACK = ("feedback", _("Feedback"))


class ContactMethods(models.TextChoices):
    """
    Contact Methods
    """

    EMAIL = ("email", _("Email"))
    PHONE = ("phone", _("Phone"))
    TEXT = ("text", _("Text Message"))
