from django.contrib import admin
from .models import Settings

""" Admin view for Settings """


@admin.register(Settings)
class CiscoDNACNetBoxAdmin(admin.ModelAdmin):
    list_display = ("hostname", "username", "status")
