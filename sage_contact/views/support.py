from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin


class SupportRequestViewMixin(ContextMixin):
    """
    A mixin to add contact form functionality to a view.

    This mixin provides functionalities for handling the contact form.
    It can be mixed into any Django view to add these capabilities.
    """

    support_form_class = None
    support_success_url_name = None
    support_form_context_name = "contact_form"
    support_form_success_message = _(
        "Thank you for contacting us! We will be in touch soon."
    )
    template_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.get_support_form_class():
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the 'support_form_class' attribute. "
                "You must define 'support_form_class' in your view or override 'get_support_form_class' method."
            )
        if not self.support_success_url_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the 'support_success_url_name' attribute. "
                "You must define 'support_success_url_name' in your view."
            )
        if not self.support_form_context_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the 'support_form_context_name' attribute. "
                "You must define 'support_form_context_name' in your view."
            )
        if not self.get_support_form_success_message():
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the 'support_form_success_message' attribute. "
                "You must define 'support_form_success_message' in your view or override 'get_support_form_success_message' method."
            )
        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the 'template_name' attribute. "
                "You must define 'template_name' in your view or override 'get_template_name' method."
            )

    def get_support_form_class(self):
        """Returns the form class to use in this view."""
        return self.support_form_class

    def get_support_form_success_message(self):
        """Returns the success message to display upon successful form submission."""
        return self.support_form_success_message

    def get_success_url(self):
        """Returns the URL to redirect to after successful form submission."""
        return reverse(self.support_success_url_name)

    def get_template_name(self):
        """Returns the template name to use for rendering the view."""
        return self.template_name

    def get_context_data(self, **kwargs):
        """Adds the form to the context."""
        context = super().get_context_data(**kwargs)
        context[self.support_form_context_name] = self.get_support_form_class()()
        return context

    def post(self, request, *args, **kwargs):
        """Handles POST requests, validates and processes the form."""
        contact_form = self.get_support_form_class()(request.POST)
        if contact_form.is_valid():
            try:
                contact_form.save()
                messages.success(request, self.get_support_form_success_message())
                return redirect(self.get_success_url())
            except Exception as e:
                messages.error(
                    request,
                    _("There was an error processing your request. Please try again."),
                )
                # Log the exception, e.g., logging.error(e)
        context = self.get_context_data(**kwargs)
        context[self.support_form_context_name] = contact_form
        return render(request, self.get_template_name(), context)
