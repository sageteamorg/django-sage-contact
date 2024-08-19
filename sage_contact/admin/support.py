from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from sage_contact.models import (
    FullSupportRequest,
    SupportRequestBase,
    SupportRequestWithLocation,
    SupportRequestWithPhone,
)

class SupportRequestBaseChildAdmin(PolymorphicParentModelAdmin, admin.ModelAdmin):
    base_model = SupportRequestBase
    search_fields = ["subject", "full_name", "email"]
    search_help_text = _("Search by subject, full name, or email")
    list_display = ["subject", "full_name", "email", "created_at", "modified_at", "get_request_type"]
    list_filter = ["created_at", "modified_at"]
    save_on_top = True
    readonly_fields = ["created_at", "modified_at"]
    fieldsets = (
        (
            _("Contact Information"),
            {"fields": ("subject", "full_name", "email", "message")},
        ),
        (_("Timestamps"), {"fields": ("created_at", "modified_at")}),
    )

    def get_request_type(self, obj):
        return obj.get_real_instance_class()._meta.verbose_name

    get_request_type.short_description = _("Request Type")


@admin.register(SupportRequestBase)
class SupportRequestBaseParentAdmin(PolymorphicChildModelAdmin, SupportRequestBaseChildAdmin):
    base_model = SupportRequestBase
    show_in_index = True
    child_models = (
        SupportRequestWithPhone,
        SupportRequestWithLocation,
        FullSupportRequest,
    )
    list_display = [
        "subject",
        "full_name",
        "email",
        "created_at",
        "modified_at",
        "get_request_type",
    ]
    list_filter = [
        "created_at",
        "modified_at",
        "polymorphic_ctype",
    ]
    search_fields = ["subject", "full_name", "email"]
    search_help_text = _("Search by subject, full name, or email")
    save_on_top = True
    readonly_fields = ["created_at", "modified_at"]

    def has_module_permission(self, request):
        return False


@admin.register(SupportRequestWithPhone)
class SupportRequestWithPhoneAdmin(PolymorphicChildModelAdmin, SupportRequestBaseChildAdmin):
    base_model = SupportRequestWithPhone
    show_in_index = True
    list_display = [
        "subject",
        "full_name",
        "email",
        "phone_number",
        "created_at",
        "modified_at",
        "get_request_type",
    ]
    fieldsets = (
        (
            _("Contact Information"),
            {"fields": ("subject", "full_name", "email", "phone_number", "message")},
        ),
        (_("Timestamps"), {"fields": ("created_at", "modified_at")}),
    )

    def has_module_permission(self, request):
        return False


@admin.register(SupportRequestWithLocation)
class SupportRequestWithLocationAdmin(PolymorphicChildModelAdmin, SupportRequestBaseChildAdmin):
    base_model = SupportRequestWithLocation
    show_in_index = True
    list_display = [
        "subject",
        "full_name",
        "email",
        "phone_number",
        "country",
        "ip_address",
        "created_at",
        "modified_at",
        "get_request_type",
    ]
    fieldsets = (
        (
            _("Contact Information"),
            {
                "fields": (
                    "subject",
                    "full_name",
                    "email",
                    "phone_number",
                    "message",
                    "country",
                    "ip_address",
                )
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "modified_at")}),
    )

    def has_module_permission(self, request):
        return False


@admin.register(FullSupportRequest)
class FullSupportRequestAdmin(PolymorphicChildModelAdmin, SupportRequestBaseChildAdmin):
    show_in_index = True
    base_model = FullSupportRequest
    list_display = [
        "subject",
        "full_name",
        "email",
        "phone_number",
        "country",
        "user",
        "contacted_before",
        "contact_reason",
        "preferred_contact_method",
        "created_at",
        "modified_at",
        "get_request_type",
    ]
    autocomplete_fields = ("user",)
    fieldsets = (
        (
            _("Contact Information"),
            {
                "fields": (
                    "subject",
                    "full_name",
                    "email",
                    "phone_number",
                    "message",
                    "country",
                    "ip_address",
                    "user",
                    "contacted_before",
                    "contact_reason",
                    "preferred_contact_method",
                )
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "modified_at")}),
    )

    def has_module_permission(self, request):
        return False
