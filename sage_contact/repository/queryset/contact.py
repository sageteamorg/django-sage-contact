from django.db import models
from django.db.models import QuerySet


class LabelQuerySet(QuerySet):
    """
    Custom QuerySet for the Label model.
    """

    def search_by_name(self, name: str) -> QuerySet:
        """
        Search labels by name.

        :param name: The name to search for.
        :return: A QuerySet of matching labels.
        """
        return self.filter(name__icontains=name)

    def order_by_name(self) -> QuerySet:
        """
        Order labels by name.

        :return: A QuerySet of labels ordered by name.
        """
        return self.order_by("name")


class ContactQuerySet(QuerySet):
    """
    Custom QuerySet for the Contact model.
    """

    def search_by_name(self, name: str) -> QuerySet:
        """
        Search contacts by name.

        :param name: The name to search for.
        :return: A QuerySet of matching contacts.
        """
        return self.filter(
            models.Q(first_name__icontains=name) | models.Q(last_name__icontains=name)
        )

    def order_by_name(self) -> QuerySet:
        """
        Order contacts by name.

        :return: A QuerySet of contacts ordered by last name, then first name.
        """
        return self.order_by("last_name", "first_name")

    def with_email(self) -> QuerySet:
        """
        Filter contacts that have an email address.

        :return: A QuerySet of contacts with an email address.
        """
        return self.exclude(email="")

    def with_phone_number(self) -> QuerySet:
        """
        Filter contacts that have a phone number.

        :return: A QuerySet of contacts with a phone number.
        """
        return self.exclude(phone_number="")


class CustomFieldQuerySet(QuerySet):
    """
    Custom QuerySet for the CustomField model.
    """

    def search_by_field_name(self, field_name: str) -> QuerySet:
        """
        Search custom fields by field name.

        :param field_name: The field name to search for.
        :return: A QuerySet of matching custom fields.
        """
        return self.filter(field_name__icontains=field_name)

    def order_by_field_name(self) -> QuerySet:
        """
        Order custom fields by field name.

        :return: A QuerySet of custom fields ordered by field name.
        """
        return self.order_by("field_name")


class ContactLabelQuerySet(QuerySet):
    """
    Custom QuerySet for the ContactLabel model.
    """

    def search_by_contact(self, contact_id: int) -> QuerySet:
        """
        Search contact labels by contact ID.

        :param contact_id: The ID of the contact.
        :return: A QuerySet of matching contact labels.
        """
        return self.filter(contact_id=contact_id)

    def search_by_label(self, label_id: int) -> QuerySet:
        """
        Search contact labels by label ID.

        :param label_id: The ID of the label.
        :return: A QuerySet of matching contact labels.
        """
        return self.filter(label_id=label_id)
