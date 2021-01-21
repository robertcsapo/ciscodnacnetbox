import django_tables2 as tables
from django_tables2.utils import A
from django.utils.safestring import mark_safe
from utilities.tables import (
    BaseTable,
    BooleanColumn,
    ToggleColumn,
)
from .models import Settings


class MaskedPassword(tables.Column):
    def render(self, value):
        value = "*****"
        return mark_safe(value)


class SettingsTable(BaseTable):
    pk = ToggleColumn()
    hostname = tables.LinkColumn(
        "plugins:ciscodnacnetbox:settings_edit", args=[A("pk")]
    )
    username = tables.Column()
    password = MaskedPassword()
    version = tables.Column()
    verify = BooleanColumn()
    status = BooleanColumn()

    class Meta(BaseTable.Meta):
        model = Settings
        fields = [
            "pk",
            "hostname",
            "username",
            "password",
            "version",
            "verify",
            "status",
        ]
