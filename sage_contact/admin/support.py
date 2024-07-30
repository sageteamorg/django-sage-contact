from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sage_contact.models import (
    SupportRequestBase,
    SupportRequestWithLocation,
    SupportRequestWithPhone,
    FullSupportRequest
)

@admin.register(SupportRequestBase)
class SupportRequestBaseAdmin(admin.ModelAdmin):
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


@admin.register(SupportRequestWithPhone)
class SupportRequestWithPhoneAdmin(SupportRequestBaseAdmin):
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
class SupportRequestWithLocationAdmin(SupportRequestBaseAdmin):
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
                'ip_address',
                'ip_country'
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
class FullSupportRequestAdmin(SupportRequestBaseAdmin):
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
        # "country"
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
                'ip_country',
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
