# azure_token_webhook.py

import requests
from azure.core.exceptions import ClientAuthenticationError, ServiceRequestError
from azure.identity import ClientSecretCredential


class EntraTokenWebhookClient:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, scope: str):
        """
        Scope is defined as https://management.azure.com/.default
        """
        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )
        self.scope = scope

    def get_token(self) -> str:
        try:
            token = self.credential.get_token(self.scope)
            return token.token
        except ClientAuthenticationError as e:
            # bad tenant/client/secret, invalid scope, consent issues, etc
            raise RuntimeError(
                f"Failed to authenticate to Entra ID to obtain token for scope '{self.scope}'"
            ) from e
        except ServiceRequestError as e:
            # network/DNS/TLS issues reaching Entra endpoints
            raise RuntimeError(
                "Network error while requesting token from Entra ID"
            ) from e

    def post_to_webhook(
        self, webhook_url: str, payload: dict, extra_headers: dict | None = None
    ):
        access_token = self.get_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        if extra_headers:
            headers.update(extra_headers)

        resp = requests.post(webhook_url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp


TeamsAlertClient = EntraTokenWebhookClient

__all__ = ["EntraTokenWebhookClient", "TeamsAlertClient"]
