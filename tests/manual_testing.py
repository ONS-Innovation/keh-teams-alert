"""
This file is for manual testing of the package. This is useful for testing things during development.
A TeamsAlertClient instance is already setup which can be used to test the functionality of the package.

To run this file, you will need the following environment variables set:

- `TEAMS_TENANT_ID`: The tenant ID for the Microsoft Azure Active Directory.
- `TEAMS_CLIENT_ID`: The client ID for the Microsoft Azure Active Directory application.
- `TEAMS_CLIENT_SECRET`: The client secret for the Microsoft Azure Active Directory application.
- `TEAMS_WEBHOOK_URL`: The webhook URL for the Microsoft Teams channel you want to send alerts to.
- `TEAMS_CHANNEL`: The name of the Microsoft Teams channel you want to send alerts to.

Note: Changes to this file should **not** be committed to the repository.
"""

from os import environ

from keh_teams_alert import TeamsAlertClient

# Validate Environment Variables

REQUIRED_ENV_VARS = [
    "TEAMS_TENANT_ID",
    "TEAMS_CLIENT_ID",
    "TEAMS_CLIENT_SECRET",
    "TEAMS_WEBHOOK_URL",
    "TEAMS_CHANNEL",
]

missing_env_vars = [env_var for env_var in REQUIRED_ENV_VARS if env_var not in environ]

if missing_env_vars:
    raise OSError(
        "One or more required environment variables are not set. "
        f"Missing: {', '.join(missing_env_vars)}."
    )

# Get Environment Variables

TEAMS_TENANT_ID = environ["TEAMS_TENANT_ID"]
TEAMS_CLIENT_ID = environ["TEAMS_CLIENT_ID"]
TEAMS_CLIENT_SECRET = environ["TEAMS_CLIENT_SECRET"]
TEAMS_WEBHOOK_URL = environ["TEAMS_WEBHOOK_URL"]
TEAMS_CHANNEL = environ["TEAMS_CHANNEL"]

# Initialize TeamsAlertClient

client = TeamsAlertClient(
    tenant_id=TEAMS_TENANT_ID,
    client_id=TEAMS_CLIENT_ID,
    client_secret=TEAMS_CLIENT_SECRET,
    scope="https://management.azure.com/.default",
)

# Example usage

payload = {
    "channel": TEAMS_CHANNEL,
    "message": "This is a testing message from `manual_testing.py` within the keh_teams_alert package.",
}

client.post_to_webhook(webhook_url=TEAMS_WEBHOOK_URL, payload=payload)
