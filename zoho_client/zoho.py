import requests
from requests import Response
from .models import ZohoToken
from django.conf import settings


class ZohoClient:
    def __init__(self):
        self.client_id = settings.ZOHO_CLIENT_ID
        self.client_secret = settings.ZOHO_CLIENT_SECRET
        self.token_url = "https://accounts.zoho.com/oauth/v2/token"
        self.api_version = getattr(settings, "ZOHO_API_VERSION", "v2.1")
        self.base_url = getattr(settings, "ZOHO_BASE_URL", "https://zohoapis.com")
        self.headers = {}

        try:
            token = ZohoToken.objects.latest("timestamp")
            self.refresh_token = token.refresh_token
            self.access_token = token.access_token
        except ZohoToken.DoesNotExist:
            self.refresh_token = None
            self.access_token = None

    def make_request(self, method="GET", api_endpoint=None, **kwargs) -> Response:
        if not self.access_token:
            self.refresh_access_token()
        url = f"{self.base_url}/crm/{self.api_version}/{api_endpoint}"
        print(url)
        response = requests.request(method, url, headers=self.headers, **kwargs)

        # If the access token has expired, refresh it and try the request again
        if response.status_code == 401:
            self.refresh_access_token()
            return self.make_request(method, api_endpoint, **kwargs)

        return response

    def refresh_access_token(self):
        data = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
        }

        response = requests.post(self.token_url, data=data)
        self.access_token = response.json().get("access_token")

        # Save the new tokens to the database
        ZohoToken.objects.create(
            access_token=self.access_token, refresh_token=self.refresh_token
        )

        self.headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

    def fetch_tokens(self, authorization_code):
        data = {
            "code": authorization_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": "http://localhost",  # Or your actual redirect URI
            "grant_type": "authorization_code",
        }

        response = requests.post(self.token_url, data=data)
        response_data = response.json()

        if response.status_code == 200 and "refresh_token" in response_data:
            self.refresh_token = response_data["refresh_token"]
            self.access_token = response_data["access_token"]

            # Save the new tokens to the database
            ZohoToken.objects.create(
                access_token=self.access_token, refresh_token=self.refresh_token
            )

            return self.refresh_token

        else:
            # Handle error
            error = response_data.get("error", "Unknown error")
            raise Exception(f"Failed to fetch tokens: {error}")
