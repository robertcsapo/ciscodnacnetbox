# ciscodnacnetbox

![PyPI - Downloads](https://img.shields.io/pypi/dm/ciscodnacnetbox)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/ciscodnacnetbox)
![PyPI](https://img.shields.io/pypi/v/ciscodnacnetbox)

*Cisco DNA Center Integration with NetBox*

---

```ciscodnacnetbox``` is a NetBox Plugin for Cisco DNA Center.  
It uses the Cisco DNA Center Platform APIs to sync data.

## Prerequisites
- Cisco DNA Center
    - Supported release: 1.3.3+
- NetBox
    - Supported release: 2.10+
- Python
  - Version: 3.3+

## Data that is synced
- [x] Sites
- [x] Devices
- [x] IP Address (/32 of Devices)

## Screenshots
### Settings  
![](./img/settings_add.png)  
![](./img/settings.png)
### Status  
![](./img/status.png)
### Sync  
![](./img/task.png)  
![](./img/sync.png)
### NetBox Inventory
![](./img/sites.png)  
![](./img/devices.png)

## Getting Started

- Install the plugin from PyPi
    - ```pip install ciscodnacnetbox```

- Enable the plugin in ```configuration.py``` of NetBox
    ```
    PLUGINS = [
        'ciscodnacnetbox',
    ]
    ```
(More details at https://netbox.readthedocs.io/en/stable/plugins/)

If using Docker with NetBox, follow instructions on https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

## Sync your data from Cisco DNA Center to NetBox

* Add your Cisco DNA Center(s) in Settings at the ciscodnacnetbox plugin
* Check status dashboard that API calls are OK towards your Cisco DNA Center (refresh if being cached)
* Use the buttons on the Dashboard to sync (Sites is mandatory for Devices to be assigned in Netbox)

## Technologies & Frameworks Used

**Cisco Products & Services:**

- [Cisco DNA Center](https://developer.cisco.com/docs/dna-center/#!cisco-dna-center-platform-overview)

**Third-Party Products & Services:**

- [NetBox](https://github.com/netbox-community/netbox)

**Tools & Frameworks:**

- [dnacentersdk](https://github.com/cisco-en-programmability/dnacentersdk) (Python SDK)
- [django](https://www.djangoproject.com/)

## Authors & Maintainers

- Robert Csapo <rcsapo@cisco.com>

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
