# from django import forms
# from django.utils.translation import gettext_lazy as _
# from utilities.forms import BootstrapMixin, StaticSelect
from netbox.forms import NetBoxModelForm
from .models import Settings


class SettingsForm(NetBoxModelForm):
    class Meta:
        model = Settings
        fields = [
            "hostname",
            "username",
            "password",
            "version",
            "verify",
            "status",
        ]
