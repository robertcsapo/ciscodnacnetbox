import re
from django_rq import get_worker
from django_rq.queues import get_connection
from extras.models import Tag
from dcim.models import Site
from tenancy.models import Tenant

class Plugin:
    name = "ciscodnacnetbox"
    version = "1.0"
    description = "Cisco DNA Center Integration with NetBox"
    author = "Robert Csapo"
    author_email = "rcsapo@cisco.com"

class System:
    """
    Support functions for the Plugin
    """

    class Check:
        @classmethod
        def tenant(cls, tenant):
            return Tenant.objects.filter(name=tenant).exists()

        @classmethod
        def sites(cls, tenant):
            if cls.tenant(tenant):
                t = Tenant.objects.get(name=tenant).id
                if Site.objects.filter(tenant=t).exists():
                    return True
            return False

    class PluginTag:
        @staticmethod
        def get():
            return Tag.objects.get(slug="cisco-dna-center")

        @staticmethod
        def filter():
            return Tag.objects.filter(slug="cisco-dna-center")

    class Slug:
        def create(input):
            return re.sub(r"[\s\/]+", "-", input).lower()

    class RQ:
        @staticmethod
        def status():
            if get_worker("default").count(get_connection("default")) == 0:
                return False
            return True
