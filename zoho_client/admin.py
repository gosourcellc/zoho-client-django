from django.contrib import admin

from .models import ZohoToken


@admin.register(ZohoToken)
class ZohoTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "access_token", "refresh_token", "timestamp")
