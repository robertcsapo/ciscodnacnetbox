from django.urls import path
from . import views

urlpatterns = (
    # Settings
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("settings/add/", views.SettingsEdit.as_view(), name="settings_add"),
    path("settings/<int:pk>/edit/", views.SettingsEdit.as_view(), name="settings_edit"),
    path(
        "settings/<int:pk>/delete/",
        views.SettingsDelete.as_view(),
        name="settings_delete",
    ),
    path(
        "settings/delete/",
        views.SettingsDeleteBulk.as_view(),
        name="settings_delete_bulk",
    ),
    # Status
    path("status/", views.StatusView.as_view(), name="status"),
    # Tenant Data
    path("devices/", views.DeviceView.as_view(), name="devices"),
    path("<int:pk>/devices/", views.DeviceView.as_view(), name="devices"),
    path("sites/", views.SitesView.as_view(), name="sites"),
    path("<int:pk>/sites/", views.SitesView.as_view(), name="sites"),
    # Sync
    path("sync/full/", views.SyncFull.as_view(), name="sync_full"),
    path("sync/full/<uuid:id>/", views.SyncFull.as_view(), name="sync_full"),
    path(
        "sync/full/<uuid:id>/failed/",
        views.SyncFullFailed.as_view(),
        name="sync_full_failed",
    ),
    path("sync/<int:pk>/full/", views.SyncFull.as_view(), name="sync_full"),
    path("sync/sites/", views.SyncSites.as_view(), name="sync_sites"),
    path("sync/<int:pk>/sites/", views.SyncSites.as_view(), name="sync_sites"),
    path(
        "sync/devices/",
        views.SyncDevices.as_view(),
        name="sync_devices",
    ),
    path(
        "sync/<int:pk>/devices/",
        views.SyncDevices.as_view(),
        name="sync_devices",
    ),
    # Jobs
    path("job/<uuid:id>/", views.JobStatus.as_view(), name="job_status"),
    # Purge
    path("purge/<int:pk>/tenant/", views.PurgeTenant.as_view(), name="purge_tenant"),
)
