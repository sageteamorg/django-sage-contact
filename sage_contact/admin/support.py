from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from polymorphic.admin import PolymorphicChildModelAdmin

from sage_contact.models import (
    SupportRequestBase,
    SupportRequestWithLocation,
    SupportRequestWithPhone,
    FullSupportRequest
)

class SupportRequestBaseChildAdmin(PolymorphicChildModelAdmin, admin.ModelAdmin):
    base_model = SupportRequestBase
    search_fields = [
        'subject',
        'full_name',
        'email'
    ]
    search_help_text = _("Search by subject, full name, or email")
    list_display = [
        'subject', 
        'full_name',
        'email',
        'created_at',
        'modified_at'
    ]
    list_filter = [
        'created_at',
        'modified_at'
    ]
    save_on_top = True
    readonly_fields = [
        'created_at',
        'modified_at'
    ]
    fieldsets = (
        (_('Contact Information'), {
            'fields': ('subject', 'full_name', 'email', 'message')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'modified_at')
        }),
    )


@admin.register(SupportRequestBase)
class SupportRequestBaseParentAdmin(SupportRequestBaseChildAdmin):
    base_model = SupportRequestBase
    child_models = (
        SupportRequestWithPhone,
        SupportRequestWithLocation,
        FullSupportRequest,
    )
    list_display = [
        'subject',
        'full_name',
        'email',
        'created_at',
        'modified_at',
        'polymorphic_ctype',
    ]
    list_filter = [
        'created_at',
        'modified_at',
        'polymorphic_ctype',
    ]
    search_fields = [
        'subject',
        'full_name',
        'email'
    ]
    search_help_text = _("Search by subject, full name, or email")
    save_on_top = True
    readonly_fields = [
        'created_at',
        'modified_at'
    ]


@admin.register(SupportRequestWithPhone)
class SupportRequestWithPhoneAdmin(SupportRequestBaseChildAdmin):
    base_model = SupportRequestWithPhone
    list_display = [
        'subject',
        'full_name',
        'email',
        'phone_number',
        'created_at',
        'modified_at'
    ]
    fieldsets = (
        (_('Contact Information'), {
            'fields': ('subject', 'full_name', 'email', 'phone_number', 'message')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'modified_at')
        }),
    )


@admin.register(SupportRequestWithLocation)
class SupportRequestWithLocationAdmin(SupportRequestBaseChildAdmin):
    base_model = SupportRequestWithLocation
    list_display = [
        'subject',
        'full_name',
        'email',
        'phone_number',
        'country',
        'ip_address',
        'created_at',
        'modified_at'
    ]
    fieldsets = (
        (_('Contact Information'), {
            'fields': (
                'subject',
                'full_name',
                'email',
                'phone_number',
                'message',
                'country',
                'ip_address'
            )
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'modified_at'
            )
        }),
    )


@admin.register(FullSupportRequest)
class FullSupportRequestAdmin(SupportRequestBaseChildAdmin):
    base_model = FullSupportRequest
    list_display = [
        'subject',
        'full_name',
        'email',
        'phone_number',
        'country',
        'user',
        'contacted_before',
        'contact_reason',
        'preferred_contact_method',
        'created_at',
        'modified_at'
    ]
    autocomplete_fields = (
        "user",
    )
    fieldsets = (
        (_('Contact Information'), {
            'fields': (
                'subject',
                'full_name',
                'email',
                'phone_number',
                'message',
                'country',
                'ip_address',
                'user',
                'contacted_before',
                'contact_reason',
                'preferred_contact_method'
            )
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'modified_at'
            )
        }),
    )
