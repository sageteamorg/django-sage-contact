from django.core.checks import Error, register
from django.conf import settings
import os

@register()
def check_geoip_path(app_configs, **kwargs):
    errors = []
    geoip_path = getattr(settings, 'GEOIP_PATH', None)
    
    if geoip_path is not None and not os.path.exists(geoip_path):
        errors.append(
            Error(
                'GEOIP_PATH is set to a non-existent path',
                hint='Ensure the path set in GEOIP_PATH exists.',
                id='geoip.E002',
            )
        )
    
    return errors
