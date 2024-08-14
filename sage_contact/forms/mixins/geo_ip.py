import logging

from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2

logger = logging.getLogger(__name__)


class GeoLocationMixin:
    def set_ip_address(self, instance):
        ip_address = self.request.META.get("REMOTE_ADDR")
        if ip_address:
            instance.ip_address = ip_address

    def set_country_from_ip(self, instance):
        geoip_path = getattr(settings, "GEOIP_PATH", None)
        if geoip_path is None:
            logger.info("GEOIP_PATH is not set. Skipping country setting.")
            return

        ip_address = instance.ip_address
        if ip_address:
            try:
                g = GeoIP2()
                country = g.country(ip_address)["country_code"]
                instance.country = country
            except Exception as e:
                logger.warning(
                    f"Failed to get country information from GeoIP2 service: {e}"
                )
