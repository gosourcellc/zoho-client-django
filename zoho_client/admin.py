from django.contrib import admin
from django import forms
from .models import ZohoToken
from .zoho import ZohoClient

from django.shortcuts import render, redirect
from django.urls import reverse


class FetchTokensForm(forms.Form):
    authorization_code = forms.CharField()


class ZohoTokenAdmin(admin.ModelAdmin):
    list_display = ("access_token", "refresh_token", "timestamp")
    change_list_template = "admin/zoho_client/zohotoken/zoho_token_change_list.html"

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "fetch-tokens/",
                self.admin_site.admin_view(self.fetch_tokens),
                name="zoho_client_zohotoken_fetch_tokens",
            ),
        ]
        return custom_urls + urls

    def fetch_tokens(self, request):
        if request.method == "POST":
            form = FetchTokensForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data["authorization_code"]
                ZohoClient().fetch_tokens(code)
                # redirect to the ZohoToken list page
                return redirect(reverse("admin:zoho_client_zohotoken_changelist"))
        else:
            form = FetchTokensForm()

        return render(
            request, "admin/zoho_client/zohotoken/fetch_tokens.html", {"form": form}
        )


admin.site.register(ZohoToken, ZohoTokenAdmin)
