from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices


menu_items = (
    PluginMenuItem(
        link="plugins:ciscodnacnetbox:status",
        link_text="Status",
        permissions=["ciscodnacnetbox.admin_full"],
        buttons=(
            PluginMenuButton(
                link="plugins:ciscodnacnetbox:sync_full",
                title="Settings",
                icon_class="mdi mdi-all-inclusive",
                color=ButtonColorChoices.BLUE,
                permissions=["ciscodnacnetbox.admin_full"],
            ),
            PluginMenuButton(
                link="plugins:ciscodnacnetbox:settings",
                title="Settings",
                icon_class="mdi mdi-cog",
                color=ButtonColorChoices.BLUE,
                permissions=["ciscodnacnetbox.admin_full"],
            ),
        ),
    ),
)
