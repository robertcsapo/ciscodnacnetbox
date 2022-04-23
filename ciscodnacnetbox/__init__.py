from extras.plugins import PluginConfig
from .metadata import App


class CiscoDNACenterConfig(PluginConfig):
    version = App._VERSION_
    name = App._NAME_
    verbose_name = "Cisco DNA Center Sync Plugin"
    description = App._DESC_
    author = App._AUTHOR_
    author_email = App._EMAIL_
    required_settings = []
    default_settings = {}
    base_url = App._NAME_
    caching_config = {}


config = CiscoDNACenterConfig
