from decimal import Decimal
import ipaddress
from django.shortcuts import get_object_or_404
from extras.models import Tag
from dcim.models import Site, Device, DeviceRole, DeviceType, Manufacturer
from ipam.models import IPAddress
from dcim.choices import DeviceStatusChoices
from tenancy.models import Tenant
from utilities.choices import ColorChoices
from .utilities import System


class Netbox:
    class Sync:
        """
        Sync data to NetBox Models
        """

        @staticmethod
        def tenants(**kwargs):
            """
            Create Tenant based on Cisco DNA Center Instance
            """
            if "system" in kwargs["task"]:
                if Tenant.objects.filter(name=kwargs["tenant"]).exists() is False:
                    Tenant.objects.create(
                        name=kwargs["tenant"],
                        slug=kwargs["slug"],
                        description="Managed by {}".format(
                            kwargs["tenant"],
                        ),
                    )
                else:
                    Tenant.objects.filter(name=kwargs["tenant"]).update(
                        description="Managed by {}".format(
                            kwargs["tenant"],
                        ),
                    )
                return Tenant.objects.get(name=kwargs["tenant"])

        @staticmethod
        def tags(**kwargs):
            """
            Handle Tag operations with NetBox
            """
            if "system" in kwargs["task"]:
                # Create mandatory Cisco DNA Center Tag
                if len(System.PluginTag.filter()) == 0:
                    Tag.objects.create(
                        name="Cisco DNA Center",
                        slug="cisco-dna-center",
                        color=ColorChoices.COLOR_BLUE,
                        description="Managed by ciscodnacnetbox",
                    )
                else:
                    System.PluginTag.filter().update(
                        name="Cisco DNA Center",
                        description="Managed by ciscodnacnetbox",
                    )
                return System.PluginTag.get()
            elif "update" in kwargs["task"]:
                # Get Object before saving Tag
                if kwargs["model"].lower() == "Tenant".lower():
                    __obj = Tenant.objects.get(name=kwargs["filter"])
                if kwargs["model"].lower() == "DeviceType".lower():
                    __obj = DeviceType.objects.get(slug=kwargs["filter"])
                if kwargs["model"].lower() == "DeviceRole".lower():
                    __obj = DeviceRole.objects.get(name=kwargs["filter"])
                if kwargs["model"].lower() == "Device".lower():
                    __obj = Device.objects.get(serial=kwargs["filter"])
                if kwargs["model"].lower() == "IPAddress".lower():
                    kwargs["filter"] = str(ipaddress.IPv4Network(kwargs["filter"])[0])
                    __obj = IPAddress.objects.get(address=kwargs["filter"])
                if kwargs["model"].lower() == "Site".lower():
                    __obj = Site.objects.get(name=kwargs["filter"])

                if kwargs["tag"] not in __obj.tags.all():
                    # Add Cisco DNA Center Tag to NetBox Object
                    __obj.tags.add(kwargs["tag"])
                    __obj.save()
            else:
                raise Exception("Not implemented yet")

        @staticmethod
        def site(tenant, site):
            """
            Handle Site operations with NetBox
            """

            # Gather site in Netbox (site name isn't unique, even with multiple tenants)
            if Site.objects.filter(name=site.siteNameHierarchy).exists() is False:
                Site.objects.create(
                    name=site.siteNameHierarchy,
                    slug=site.slug,
                    comments=site.id,
                    description="Managed by {}".format(tenant),
                    tenant=Tenant.objects.get(name=tenant),
                )
                sync = "Created"
            else:
                Site.objects.filter(name=site.siteNameHierarchy).update(
                    slug=site.slug,
                    comments=site.id,
                    description="Managed by {}".format(tenant),
                    tenant=Tenant.objects.get(name=tenant).id,
                )
                sync = "Updated"
            __obj = Site.objects.get(name=site.siteNameHierarchy)

            # Check if additional information is avaible for the site
            __save = False
            if len(site.additionalInfo) != 0:
                for additionalInfo in site.additionalInfo:
                    if "Location" in additionalInfo["nameSpace"]:
                        if additionalInfo["attributes"]["address"] is not None:
                            if __obj.physical_address != additionalInfo["attributes"]["address"]:
                                __obj.physical_address = additionalInfo["attributes"]["address"]
                                __save = True
                        if additionalInfo["attributes"]["latitude"] is not None:
                            if __obj.latitude != Decimal(additionalInfo["attributes"]["latitude"]):
                                __obj.latitude = additionalInfo["attributes"]["latitude"]
                                __save = True
                        if additionalInfo["attributes"]["longitude"] is not None:
                            if __obj.longitude != Decimal(additionalInfo["attributes"]["longitude"]):
                                __obj.longitude = additionalInfo["attributes"]["longitude"]
                                __save = True
            if __save is True:
                # Only update Change log if something is updated
                __obj.save()

            return Site.objects.get(name=site.siteNameHierarchy), sync

        @staticmethod
        def manufacturer(manufacture, tenant):
            """
            Handle Manufacturer operations with NetBox
            """

            # Gather manufacture in Netbox
            if Manufacturer.objects.filter(name=manufacture).exists() is False:
                Manufacturer.objects.create(
                    name=manufacture,
                    slug=manufacture.lower(),
                    description="Managed by {}".format(tenant),
                )
            else:
                Manufacturer.objects.filter(name=manufacture).update(
                    slug=manufacture.lower(),
                    description="Managed by {}".format(tenant),
                )
            return Manufacturer.objects.get(name=manufacture)

        @staticmethod
        def devicetype(manufacture, model, slug, tenant):
            """
            Handle DeviceType operations with NetBox
            """

            # Gather DeviceType in Netbox
            if DeviceType.objects.filter(manufacturer=manufacture, model=model).exists() is False:
                DeviceType.objects.create(
                    manufacturer=manufacture,
                    model=model,
                    slug=slug.lower(),
                    u_height=1,
                    comments="Managed by {}".format(tenant),
                )
            else:
                DeviceType.objects.filter(manufacturer=manufacture, model=model).update(
                    slug=slug.lower(),
                    comments="Managed by {}".format(tenant),
                )
            return DeviceType.objects.get(slug=slug.lower())

        @staticmethod
        def devicerole(role, slug, tenant):
            """
            Handle DeviceRole operations with NetBox
            """

            # Gather DeviceRole in Netbox
            if DeviceRole.objects.filter(name=role).exists() is False:
                DeviceRole.objects.create(
                    name=role,
                    slug=slug.lower(),
                    color=ColorChoices.COLOR_BLUE,
                    vm_role=False,
                    description="Managed by {}".format(tenant),
                )
            else:
                DeviceRole.objects.filter(name=role).update(
                    slug=slug.lower(),
                    color=ColorChoices.COLOR_BLUE,
                    vm_role=False,
                    description="Managed by {}".format(tenant),
                )
            return DeviceRole.objects.get(name=role)

        @staticmethod
        def device(tenant, device):
            """
            Handle Device operations with NetBox
            """

            # Check device reachability in Cisco DNA Center
            if device.reachabilityStatus == "Reachable":
                device.status = DeviceStatusChoices.STATUS_ACTIVE
            else:
                device.status = DeviceStatusChoices.STATUS_FAILED

            # Gather Device in Netbox
            if Device.objects.filter(serial=device.serialNumber).exists() is False:
                if Device.objects.filter(
                    primary_ip4=device.primary_ip4,
                    tenant=Tenant.objects.get(name=tenant).id,
                ).exists():
                    # There can't be duplicate IPs in one tenant.
                    # But DNAC can register duplicate IPs, if only one is Reachable
                    Device.objects.create(
                        name=device.hostname,
                        device_role=device.role,
                        device_type=device.family_type,
                        serial=device.serialNumber,
                        status=device.status,
                        site=device.site,
                        comments="Managed by {}".format(tenant),
                        tenant=Tenant.objects.get(name=tenant),
                    )
                    sync = "Error IPv4"
                    return Device.objects.get(serial=device.serialNumber), sync
                else:
                    Device.objects.create(
                        name=device.hostname,
                        device_role=device.role,
                        device_type=device.family_type,
                        primary_ip4=device.primary_ip4,
                        serial=device.serialNumber,
                        status=device.status,
                        site=device.site,
                        comments="Managed by {}".format(tenant),
                        tenant=Tenant.objects.get(name=tenant),
                    )
                    sync = "Created"
            else:
                if (
                    device.serialNumber
                    != Device.objects.get(
                        primary_ip4=device.primary_ip4,
                        tenant=Tenant.objects.get(name=tenant).id,
                    ).serial
                ):
                    # There can't be duplicate IPs in one tenant.
                    # But DNAC can register duplicate IPs, if only one is Reachable
                    Device.objects.filter(serial=device.serialNumber, tenant=Tenant.objects.get(name=tenant).id,).update(
                        name=device.hostname,
                        device_role=device.role,
                        device_type=device.family_type,
                        status=device.status,
                        site=device.site,
                        comments="Managed by {}".format(tenant),
                        tenant=Tenant.objects.get(name=tenant).id,
                    )
                    sync = "Error IPv4"
                else:
                    Device.objects.filter(serial=device.serialNumber, tenant=Tenant.objects.get(name=tenant).id,).update(
                        name=device.hostname,
                        device_role=device.role,
                        device_type=device.family_type,
                        primary_ip4=device.primary_ip4,
                        status=device.status,
                        site=device.site,
                        comments="Managed by {}".format(tenant),
                        tenant=Tenant.objects.get(name=tenant).id,
                    )
                    sync = "Updated"

            # Assign IP Address to Device in NetBox
            IPAddress.objects.filter(address=str(device.primary_ip4), tenant=Tenant.objects.get(name=tenant).id,).update(
                assigned_object_id=Device.objects.get(serial=device.serialNumber).id,
            )

            return Device.objects.get(serial=device.serialNumber), sync

        @staticmethod
        def ipaddress(tenant, address, hostname):
            """
            Handle IPAddress operations with NetBox
            """

            # Gather IPAddress in Netbox
            if IPAddress.objects.filter(address=address, tenant=Tenant.objects.get(name=tenant).id).exists() is False:
                IPAddress.objects.create(
                    address=address,
                    status=DeviceStatusChoices.STATUS_ACTIVE,
                    dns_name=hostname,
                    description="Managed by {}".format(tenant),
                    tenant=Tenant.objects.get(name=tenant),
                )
            else:
                IPAddress.objects.filter(address=address, tenant=Tenant.objects.get(name=tenant).id).update(
                    status=DeviceStatusChoices.STATUS_ACTIVE,
                    dns_name=hostname,
                    description="Managed by {}".format(tenant),
                    tenant=Tenant.objects.get(name=tenant).id,
                )
            return IPAddress.objects.get(address=address)

    class Purge:
        @staticmethod
        def database(**kwargs):
            """
            Purge data from NetBox Database - when running Sync
            """

            # Delete devices related to Tenant
            if kwargs["type"] == "devices":

                # Unique Serial Numbers in Netbox
                netbox_serials = [d.serial for d in Device.objects.filter(tenant=Tenant.objects.get(name=kwargs["tenant"]).id)]

                # Unique Serial Numbers in Cisco DNA Center Instance
                dnac_serials = []
                for d in kwargs["data"]:
                    dnac_serials.append(d["serial"])

                # Diff between NetBox and Cisco DNA Center Instance
                purge = list(set(netbox_serials) - set(dnac_serials))

                if len(purge) == 0:
                    return False
                else:

                    # Remove diff in NetBox
                    try:
                        for serial in purge:
                            Device.objects.filter(id=Device.objects.get(serial=serial).id).delete()
                        return True
                    except Exception as error_msg:
                        print("Error couldn't delete {}\n{}".format(kwargs["data"], error_msg))
                        return False
            # Delete sites related to Tenant
            elif kwargs["type"] == "sites":

                # Unique slug/uuid in NetBox
                netbox_sites = [s.slug for s in Site.objects.filter(tenant=Tenant.objects.get(name=kwargs["tenant"]).id)]

                # Unique Site id/uuid in Cisco DNA Center Instance
                dnac_sites = []
                for s in kwargs["data"]:
                    dnac_sites.append(s["slug"])

                # Diff between NetBox and Cisco DNA Center Instance
                purge = list(set(netbox_sites) - set(dnac_sites))

                if len(purge) == 0:
                    return False
                else:

                    # Remove diff in NetBox
                    try:
                        for uuid in purge:
                            Site.objects.filter(slug=uuid).delete()
                        return True
                    except Exception as error_msg:
                        print("Error couldn't delete {}\n{}".format(kwargs["data"], error_msg))
                        return False
            else:
                raise Exception("Not implemented yet")

        @classmethod
        def tenant(cls, **kwargs):
            """
            Delete Tenant related to Cisco DNA Center Instance
            """

            # Get NetBox tenants based on Cisco DNA Center Tag
            results = {}
            dnac_tag = System.PluginTag.get()
            tenant_name = get_object_or_404(Tenant, pk=kwargs["pk"], tags=dnac_tag).name

            # Delete objects based on dependencies until Tenant is deleted
            results[tenant_name] = {}
            results[tenant_name]["devices"] = cls.devices(**kwargs)
            results[tenant_name]["ipaddress"] = cls.ipaddress(**kwargs)
            results[tenant_name]["sites"] = cls.sites(**kwargs)
            Tenant.objects.filter(pk=kwargs["pk"]).delete()

            return results

        @classmethod
        def devices(cls, **kwargs):
            """
            Delete Devices related to Cisco DNA Center Instance
            """
            result = Device.objects.filter(tenant=kwargs["pk"]).count()
            Device.objects.filter(tenant=kwargs["pk"]).delete()
            return result

        @classmethod
        def ipaddress(cls, **kwargs):
            """
            Delete IPAddress related to Cisco DNA Center Instance
            """
            result = IPAddress.objects.filter(tenant=kwargs["pk"]).count()
            IPAddress.objects.filter(tenant=kwargs["pk"]).delete()
            return result

        @classmethod
        def sites(cls, **kwargs):
            """
            Delete Sites related to Cisco DNA Center Instance
            """
            result = Site.objects.filter(tenant=kwargs["pk"]).count()
            Site.objects.filter(tenant=kwargs["pk"]).delete()
            return result
