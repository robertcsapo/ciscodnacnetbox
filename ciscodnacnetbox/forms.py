from utilities.forms import BootstrapMixin, StaticSelect2
from extras.forms import CustomFieldModelForm
from .models import Settings


class SettingsForm(BootstrapMixin, CustomFieldModelForm):
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
        widgets = {
            "status": StaticSelect2(
                choices=(
                    ("True", "Yes"),
                    ("False", "No"),
                )
            ),
            "verify": StaticSelect2(
                choices=(
                    (True, "Yes"),
                    (False, "No"),
                )
            ),
        }
