from django.db import models
from django.db.models import QuerySet
from sage_contact.repository.queryset.contact import (
    ContactLabelQuerySet,
    ContactQuerySet,
    CustomFieldQuerySet,
    LabelQuerySet,
)


class LabelManager(models.Manager):
    """
    Custom Manager for the Label model.
    """

    def get_queryset(self) -> LabelQuerySet:
        """
        Override the default queryset with the custom LabelQuerySet.

        :return: An instance of LabelQuerySet.
        """
        return LabelQuerySet(self.model, using=self._db)

    def search_by_name(self, name: str) -> QuerySet:
        """
        Proxy method to search labels by name.

        :param name: The name to search for.
        :return: A QuerySet of matching labels.
        """
        return self.get_queryset().search_by_name(name)

    def order_by_name(self) -> QuerySet:
        """
        Proxy method to order labels by name.

        :return: A QuerySet of labels ordered by name.
        """
        return self.get_queryset().order_by_name()


class ContactManager(models.Manager):
    """
    Custom Manager for the Contact model.
    """

    def get_queryset(self) -> ContactQuerySet:
        """
        Override the default queryset with the custom ContactQuerySet.

        :return: An instance of ContactQuerySet.
        """
        return ContactQuerySet(self.model, using=self._db)

    def search_by_name(self, name: str) -> QuerySet:
        """
        Proxy method to search contacts by name.

        :param name: The name to search for.
        :return: A QuerySet of matching contacts.
        """
        return self.get_queryset().search_by_name(name)

    def order_by_name(self) -> QuerySet:
        """
        Proxy method to order contacts by name.

        :return: A QuerySet of contacts ordered by last name, then first name.
        """
        return self.get_queryset().order_by_name()

    def with_email(self) -> QuerySet:
        """
        Proxy method to filter contacts that have an email address.

        :return: A QuerySet of contacts with an email address.
        """
        return self.get_queryset().with_email()

    def with_phone_number(self) -> QuerySet:
        """
        Proxy method to filter contacts that have a phone number.

        :return: A QuerySet of contacts with a phone number.
        """
        return self.get_queryset().with_phone_number()


class CustomFieldManager(models.Manager):
    """
    Custom Manager for the CustomField model.
    """

    def get_queryset(self) -> CustomFieldQuerySet:
        """
        Override the default queryset with the custom CustomFieldQuerySet.

        :return: An instance of CustomFieldQuerySet.
        """
        return CustomFieldQuerySet(self.model, using=self._db)

    def search_by_field_name(self, field_name: str) -> QuerySet:
        """
        Proxy method to search custom fields by field name.

        :param field_name: The field name to search for.
        :return: A QuerySet of matching custom fields.
        """
        return self.get_queryset().search_by_field_name(field_name)

    def order_by_field_name(self) -> QuerySet:
        """
        Proxy method to order custom fields by field name.

        :return: A QuerySet of custom fields ordered by field name.
        """
        return self.get_queryset().order_by_field_name()


class ContactLabelManager(models.Manager):
    """
    Custom Manager for the ContactLabel model.
    """

    def get_queryset(self) -> ContactLabelQuerySet:
        """
        Override the default queryset with the custom ContactLabelQuerySet.

        :return: An instance of ContactLabelQuerySet.
        """
        return ContactLabelQuerySet(self.model, using=self._db)

    def search_by_contact(self, contact_id: int) -> QuerySet:
        """
        Proxy method to search contact labels by contact ID.

        :param contact_id: The ID of the contact.
        :return: A QuerySet of matching contact labels.
        """
        return self.get_queryset().search_by_contact(contact_id)

    def search_by_label(self, label_id: int) -> QuerySet:
        """
        Proxy method to search contact labels by label ID.

        :param label_id: The ID of the label.
        :return: A QuerySet of matching contact labels.
        """
        return self.get_queryset().search_by_label(label_id)
