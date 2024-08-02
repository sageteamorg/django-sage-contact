from django.conf import settings
from django.core.checks import Error, register
from django.template.utils import get_app_template_dirs
from typing import List, Dict, Any
import os

from .exc import DjangoSageContactError, DjangoSageContactConfigurationError


@register()
def check_django_sage_contact_config(app_configs: Dict[str, Any], **kwargs: Any) -> List[Error]:
    """
    Check the django-sage-contact and email template configuration for the application.

    This function verifies that all required settings are present and ensures the settings are correct.
    Any errors encountered during these checks are returned.

    Parameters
    ----------
    app_configs : dict
        The application configurations.
    **kwargs
        Additional keyword arguments.

    Returns
    -------
    list of Error
        A list of Error objects representing any configuration errors found.

    Examples
    --------
    >>> errors = check_geoip_path(app_configs)
    >>> if errors:
    ...     for error in errors:
    ...         print(error)
    """
    errors: List[Error] = []

    def get_settings() -> Dict[str, Any]:
        return {
            "SAGE_CONTACT_GEOIP_PATH": getattr(settings, 'SAGE_CONTACT_GEOIP_PATH', None),
            "SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM": getattr(settings, 'SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM', True),
            "SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH": getattr(settings, 'SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH', None),
            "EMAIL_HOST": getattr(settings, 'EMAIL_HOST', None),
            "EMAIL_PORT": getattr(settings, 'EMAIL_PORT', None),
            "EMAIL_HOST_USER": getattr(settings, 'EMAIL_HOST_USER', None),
            "EMAIL_HOST_PASSWORD": getattr(settings, 'EMAIL_HOST_PASSWORD', None),
            "EMAIL_USE_TLS": getattr(settings, 'EMAIL_USE_TLS', None),
            "BASE_DIR": getattr(settings, 'BASE_DIR', None),
            "DEBUG": getattr(settings, 'DEBUG', True),
        }

    def check_geoip_path_setting(geoip_path: str) -> None:
        if geoip_path and not os.path.exists(geoip_path):
            errors.append(
                Error(
                    'SAGE_CONTACT_GEOIP_PATH is set to a non-existent path',
                    hint='Ensure the path set in SAGE_CONTACT_GEOIP_PATH exists.',
                    id='geoip.E002',
                )
            )

    def check_email_template_path(send_email: bool, template_path: str, base_dir: str) -> None:
        if send_email:
            if not template_path:
                raise DjangoSageContactConfigurationError(
                    detail='SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH is not set',
                    code='E001',
                    section_code='sage_contact'
                )
            else:
                if not os.path.exists(os.path.join(base_dir, template_path)):
                    template_found = False
                    for template_dir in get_app_template_dirs('templates'):
                        if os.path.exists(os.path.join(template_dir, template_path)):
                            template_found = True
                            break
                    if not template_found:
                        raise DjangoSageContactConfigurationError(
                            detail='SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH is set to a non-existent path',
                            code='E002',
                            section_code='sage_contact'
                        )

    def check_email_settings(send_email: bool, debug: bool) -> None:
        if not debug and send_email:
            email_settings: List[str] = ['EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 'EMAIL_USE_TLS']
            for setting in email_settings:
                if not getattr(settings, setting, None):
                    raise DjangoSageContactConfigurationError(
                        detail=f'{setting} is not set. The {setting} must be set in settings because DEBUG is False and '
                               'SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM is True. Ensure all necessary '
                               'email settings are configured for the application to send emails in '
                               'production.',
                        code=f'E00{email_settings.index(setting) + 1}',
                        section_code='sage_contact'
                    )

    try:
        settings_dict: Dict[str, Any] = get_settings()
        # get settings
        geoip_path: str = settings_dict["SAGE_CONTACT_GEOIP_PATH"]
        send_email_after_sage_contact_support_form: str = settings_dict["SEND_EMAIL_AFTER_SAGE_CONTACT_SUPPORT_FORM"]
        sage_contact_support_email_template_path: str = settings_dict["SAGE_CONTACT_SUPPORT_EMAIL_TEMPLATE_PATH"]
        base_dir: str = settings_dict["BASE_DIR"]
        debug: bool = settings_dict["DEBUG"]

        check_geoip_path_setting(geoip_path)
        check_email_template_path(send_email_after_sage_contact_support_form, sage_contact_support_email_template_path, base_dir)
        check_email_settings(send_email_after_sage_contact_support_form, debug)
    except DjangoSageContactConfigurationError as e:
        errors.append(
            Error(
                str(e),
                id=f"{e.section_code}.{e.code}",
            )
        )
    except DjangoSageContactError as e:
        errors.append(
            Error(
                str(e),
                id=f"{e.section_code}.{e.code}",

            )
        )

    return errors