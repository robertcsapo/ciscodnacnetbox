from extras.plugins import PluginConfig

class CiscoDNACenterConfig(PluginConfig):
    version = "1.0"
    name = "ciscodnacnetbox"
    verbose_name = "Cisco DNA Center Sync Plugin"
    description = "Cisco DNA Center Integration with NetBox"
    author = "Robert Csapo"
    author_email = "rcsapo@cisco.com"
    required_settings = []
    default_settings = {}
    base_url = "ciscodnacnetbox"
    caching_config = {}


config = CiscoDNACenterConfig
