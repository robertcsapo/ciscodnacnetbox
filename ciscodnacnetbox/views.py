import platform
from django.conf import settings
from django.http import Http404, HttpResponseServerError, JsonResponse
from django.views.defaults import ERROR_500_TEMPLATE_NAME
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from utilities.forms import ConfirmationForm
from tenancy.models import Tenant
from netbox.views import generic
from .models import Settings
from .forms import SettingsForm
from .tables import SettingsTable
from .ciscodnac.data import Data
from .ciscodnac.netbox import Netbox
from .ciscodnac.utilities import System


class SettingsView(generic.ObjectListView):
    """
    Cisco DNA Center Settings
    """
    
    queryset = Settings.objects.all()
    table = SettingsTable
    template_name = "ciscodnacnetbox/settings.html"


class SettingsEdit(generic.ObjectEditView):
    """
    Add/Edit Cisco DNA Center Settings
    """

    queryset = Settings.objects.all()
    model_form = SettingsForm
    template_name = "ciscodnacnetbox/settings_edit.html"


class SettingsDelete(generic.ObjectDeleteView):
    """
    Delete Cisco DNA Center Settings
    """

    queryset = Settings.objects.all()


class SettingsDeleteBulk(generic.BulkDeleteView):
    """
    Delete multiple Cisco DNA Center Settings
    """

    queryset = Settings.objects.all()
    table = SettingsTable


class StatusView(View):
    """
    Plugin Status Dashboard
    """

    def get(self, request):
        # Check that NetBox tag exists for Cisco DNA Center
        Netbox.Sync.tags(task="system")

        # Check that Cisco DNA Center Settings exists
        if Settings.objects.filter().exists() is False:
            return redirect("/plugins/ciscodnacnetbox/settings/")

        data = Data.status()
        return render(
            request,
            "ciscodnacnetbox/status.html",
            {
                "dnac": data["dnac"],
                "netbox": request.build_absolute_uri("/"),
                "netbox_sites": data["netbox"]["sites"],
                "netbox_devices": data["netbox"]["devices"],
                "netbox_tenants": data["netbox"]["tenants"],
            },
        )


class SyncFull(View):
    """
    Sync Cisco DNA Center
    """

    def get(self, request, **kwargs):
        # Check that we have Cisco DNA Center settings
        if Settings.objects.filter().exists() is False:
            return redirect("/plugins/ciscodnacnetbox/settings/")

        # Check if RQ workers are running
        if System.RQ.status() is False:
            template = loader.get_template(ERROR_500_TEMPLATE_NAME)
            error_msg = """
            Addtional Workers not running for Background Tasks.
            Verify that rqworker is running.
            """
            return HttpResponseServerError(
                template.render(
                    {
                        "error": error_msg,
                        "exception": "ciscodnacnetbox plugin - RQ",
                        "netbox_version": settings.VERSION,
                        "python_version": platform.python_version(),
                    }
                )
            )

        # Run Sync as Background Job in RQ
        data = Data.sync_full(**kwargs)
        if "id" in kwargs:
            if data is None:
                raise Http404()
            return render(
                request,
                "ciscodnacnetbox/sync_full.html",
                {
                    "data": data,
                },
            )
        return render(
            request,
            "ciscodnacnetbox/loading_job.html",
            {
                "data": data,
            },
        )


class SyncFullFailed(View):
    """
    Display failed RQ Job
    """

    def get(self, request, id):
        data = Data.job_status(id)
        return render(
            request,
            "ciscodnacnetbox/sync_full_failed.html",
            {
                "data": data,
            },
        )


class JobStatus(View):
    """
    Check RQ Job Status
    """

    def get(self, request, id):
        data = Data.job_status(id)
        if data is None:
            raise Http404()
        return JsonResponse(data)


class DeviceView(View):
    """
    Cisco DNA Center Devices
    """

    def get(self, request, **kwargs):
        data = Data.devices(**kwargs)
        return render(
            request,
            "ciscodnacnetbox/devices.html",
            {
                "data": data,
            },
        )


class SyncDevices(View):
    """
    Sync Cisco DNA Center Devices
    """

    def get(self, request, **kwargs):
        data = Data.sync_devices(**kwargs)
        return render(
            request,
            "ciscodnacnetbox/sync_devices.html",
            {
                "data": data,
            },
        )


class SitesView(View):
    """
    Cisco DNA Center Sites
    """

    def get(self, request, **kwargs):
        data = Data.sites(**kwargs)
        return render(
            request,
            "ciscodnacnetbox/sites.html",
            {
                "data": data,
            },
        )


class SyncSites(View):
    """
    Sync Cisco DNA Center Sites
    """

    def get(self, request, **kwargs):
        data = Data.sync_sites(**kwargs)
        return render(
            request,
            "ciscodnacnetbox/sync_sites.html",
            {
                "data": data,
            },
        )


class PurgeTenant(View):
    """
    Purge NetBox Tenants related to Cisco DNA Center
    """

    def get(self, request, **kwargs):

        # Verify that the Tenant exists in NetBox
        tenant = get_object_or_404(Tenant, pk=kwargs["pk"], tags=System.PluginTag.get())

        # Confirm deletion
        form = ConfirmationForm(initial=request.GET)
        return render(
            request,
            "generic/object_delete.html",
            {
                "obj": tenant,
                "form": form,
                "return_url": reverse("plugins:ciscodnacnetbox:purge_tenant", args=(kwargs["pk"],)),
            },
        )

    def post(self, request, **kwargs):

        # Delete Tenant in NetBox
        data = Data.purge_tenant(**kwargs)
        return render(
            request,
            "ciscodnacnetbox/purge_tenant.html",
            {
                "data": data,
            },
        )
