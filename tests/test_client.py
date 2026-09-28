from unittest.mock import Mock, patch

import pytest
from azure.core.exceptions import ClientAuthenticationError, ServiceRequestError

from keh_teams_alert import TeamsAlertClient

TENANT_ID = "tenant-id"
CLIENT_ID = "client-id"
CLIENT_SECRET = "client-secret"
SCOPE = "https://management.azure.com/.default"


@patch("keh_teams_alert.ClientSecretCredential")
def test_initialises_credential_and_stores_scope(credential_class):
    client = TeamsAlertClient(TENANT_ID, CLIENT_ID, CLIENT_SECRET, SCOPE)

    credential_class.assert_called_once_with(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    assert client.scope == SCOPE
    assert client.credential is credential_class.return_value


@patch("keh_teams_alert.ClientSecretCredential")
def test_get_token_returns_token_value(credential_class):
    credential_class.return_value.get_token.return_value = Mock(token="access-token")
    client = TeamsAlertClient(TENANT_ID, CLIENT_ID, CLIENT_SECRET, SCOPE)

    assert client.get_token() == "access-token"
    credential_class.return_value.get_token.assert_called_once_with(SCOPE)


@pytest.mark.parametrize(
    ("azure_error", "message"),
    [
        (
            ClientAuthenticationError("invalid credentials"),
            f"Failed to authenticate to Entra ID to obtain token for scope '{SCOPE}'",
        ),
        (
            ServiceRequestError("network unavailable"),
            "Network error while requesting token from Entra ID",
        ),
    ],
)
@patch("keh_teams_alert.ClientSecretCredential")
def test_get_token_translates_azure_errors(credential_class, azure_error, message):
    credential_class.return_value.get_token.side_effect = azure_error
    client = TeamsAlertClient(TENANT_ID, CLIENT_ID, CLIENT_SECRET, SCOPE)

    with pytest.raises(RuntimeError, match=message) as raised:
        client.get_token()

    assert raised.value.__cause__ is azure_error


@patch("keh_teams_alert.requests.post")
@patch.object(TeamsAlertClient, "get_token", return_value="access-token")
def test_post_to_webhook_sends_token_payload_and_headers(get_token, post):
    response = post.return_value
    payload = {"message": "Alert"}
    client = TeamsAlertClient(TENANT_ID, CLIENT_ID, CLIENT_SECRET, SCOPE)

    result = client.post_to_webhook(
        "https://example.test/webhook",
        payload,
        extra_headers={"X-Request-ID": "request-id"},
    )

    assert result is response
    get_token.assert_called_once_with()
    post.assert_called_once_with(
        "https://example.test/webhook",
        json=payload,
        headers={
            "Authorization": "Bearer access-token",
            "Content-Type": "application/json",
            "X-Request-ID": "request-id",
        },
    )
    response.raise_for_status.assert_called_once_with()


@patch("keh_teams_alert.requests.post")
@patch.object(TeamsAlertClient, "get_token", return_value="access-token")
def test_post_to_webhook_works_without_extra_headers(get_token, post):
    client = TeamsAlertClient(TENANT_ID, CLIENT_ID, CLIENT_SECRET, SCOPE)

    client.post_to_webhook("https://example.test/webhook", {"message": "Alert"})

    post.assert_called_once_with(
        "https://example.test/webhook",
        json={"message": "Alert"},
        headers={
            "Authorization": "Bearer access-token",
            "Content-Type": "application/json",
        },
    )
    get_token.assert_called_once_with()
