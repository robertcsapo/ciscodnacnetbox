from django.shortcuts import get_object_or_404
from dnacentersdk import api
from ..models import Settings


class CiscoDNAC:

    # Get all tenants from Settings
    __tenants = Settings.objects.all().nocache()

    def __init__(self, **kwargs):
        """
        Cisco DNA Center API Instance
        """
        self.dnac = {}
        self.dnac_status = {}

        # Single Cisco DNA Center Instance
        if "pk" in kwargs and isinstance(kwargs["pk"], int) is True:

            # Verify that the Tenant exist based on the `pk`
            tenant = get_object_or_404(Settings, pk=kwargs["pk"])

            # Create Cisco DNA Center API Object
            obj = self.auth(tenant)

            # Check that Auth is successful
            if obj:
                self.dnac[tenant.hostname] = obj[1]
            return

        for tenant in self.__tenants:
            self.dnac_status[tenant.hostname] = "disabled"

            # Create Cisco DNA Center API Object if enabled
            if tenant.status is True:

                # Create Cisco DNA Center API Object
                obj = self.auth(tenant)

                # Check that Auth is successful
                if obj:
                    self.dnac[tenant.hostname] = obj[1]
        return

    def auth(self, tenant):
        """
        Cisco DNA Center API Object
        """
        try:
            obj = api.DNACenterAPI(
                username=tenant.username,
                password=tenant.password,
                base_url="https://" + tenant.hostname,
                # version="2.1.2",  # TODO
                verify=bool(tenant.verify),
            )
            self.dnac_status[tenant.hostname] = "success"
            return True, obj
        except Exception as error_msg:
            print("Error for {}: {}".format(tenant, error_msg))
            self.dnac_status[tenant.hostname] = error_msg
            return False

    def devices(self, tenant):
        """
        Get Devices from Cisco DNA Center
        """
        return tenant.devices.get_device_list().response

    def sites(self, tenant):
        """
        Get Sites from Cisco DNA Center
        """
        return tenant.sites.get_site().response

    def sites_count(self, tenant):
        """
        Get Sites count from Cisco DNA Center
        """
        return tenant.sites.get_site_count().response

    @classmethod
    def devices_to_sites(cls, tenant):
        """
        Map Device Serial Number to Site ID from Cisco DNA Center
        """
        results = {}
        for site in tenant.sites.get_site().response:
            for members in tenant.sites.get_membership(site_id=site.id).device:
                for device in members.response:
                    results[device.serialNumber] = site.id
        return results
