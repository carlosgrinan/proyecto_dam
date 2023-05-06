import os
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from google.http import BatchHttpRequestCustom


class GoogleApi:
    def __init__(
        self,
        api_name,
        api_version,
        refresh_token,
        # mock=False,
        # mock_filename=None
    ):
        # if mock:
        #     http = HttpMock(mock_filename, {"status": "200"})
        #     self.service = build(api_name, api_version, http=http)

        # else:
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
        )
        self.service = build(api_name, api_version, credentials=credentials)

    def new_batch_http_request(
        self,
    ):
        """
        Same as service.new_batch_http_request() but returns a BatchHttpRequestCustom"""
        batch = self.service.new_batch_http_request()
        return BatchHttpRequestCustom(batch)


def get_token(code):
    url = "https://oauth2.googleapis.com/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": "http://127.0.0.1:5000",  # One of the redirect URIs listed for your project in the API Console Credentials page for the given client_id. Not used but required.
    }
    response = requests.post(url, data=data)
    return response.json().get("refresh_token")
