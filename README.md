# keh-teams-alert

Python module for sending a JSON payload (`channel` and `message`) to an HTTP webhook using an Entra ID (Azure AD) access token acquired via `azure-identity`.

## Requirements

- Python **>= 3.12**
- Poetry **2.x**
- Entra ID App Registration (client credentials: tenant id, client id, client secret)
- A webhook endpoint that accepts JSON like:

  ```json
  { "channel": "some-channel", "message": "some-message" }
  ```

## Install (as a dependency in another app)

### Install from a local path (editable)

```bash
pip install -e /path/to/keh-teams-alert
```

### Build a wheel and install it

In this repo:

```bash
poetry build
```

In the consuming project:

```bash
pip install /path/to/keh-teams-alert/dist/keh_teams_alert-*.whl
```

## Development (this repo)

Install dependencies:

```bash
poetry install
```

Quick import check:

```bash
poetry run python -c "from keh_teams_alert import EntraTokenWebhookClient; print('ok')"
```

Build:

```bash
poetry build
```

## Usage

```python
from keh_teams_alert import EntraTokenWebhookClient

client = EntraTokenWebhookClient(
    tenant_id="00000000-0000-0000-0000-000000000000",
    client_id="00000000-0000-0000-0000-000000000000",
    client_secret="***",
    scope="https://management.azure.com/.default",
)

payload = {
    "channel": "alerts",
    "message": "Hello from KEH",
}

client.post_to_webhook(
    webhook_url="https://example/webhook",
    payload=payload,
)
```

## Error handling

Token acquisition errors (bad credentials/consent) and network errors are caught and re-raised as `RuntimeError` with context from the underlying Azure SDK exception.

## Documentation

This repository uses [MkDocs](https://www.mkdocs.org/) for documentation. The documentation source files are located in the `docs` directory.

### Local Development of Documentation

To run the documentation locally:

1. Install the dependencies for MkDocs.

   ```bash
   poetry install --only docs
   ```

2. Run the MkDocs development server.

   ```bash
   poetry run mkdocs serve
   ```

## Linting and Testing

### GitHub Actions

This repository has GitHub Actions workflows set up for linting and testing. The workflows are located at:

- `.github/workflows/ci-fmt.yml` for linting and formatting checks (primary language).
- `.github/workflows/ci-test.yml` for running automated tests.
- `.github/workflows/ci-docs.yml` for checking that the documentation builds correctly and has no linting or formatting issues.
- `.github/workflows/megalinter.yml` for running MegaLinter, which checks for linting and formatting issues across multiple languages and file types (this is a catch-all linter).
- `.github/workflows/deploy-docs.yml` for deploying documentation to GitHub Pages.

### Running Tests and Linters Locally

#### Primary Language (Python)

Install dependencies:

```bash
poetry install
```

Run formatting (if configured):

```bash
poetry run ruff format .
```

Run linting (if configured):

```bash
poetry run ruff check .
```

Run unit tests (if configured):

```bash
poetry run pytest -q
```

> If you don’t have `ruff`/`pytest` configured in this repo yet, add them as dev dependencies and/or update these commands to match your tooling.

#### MegaLinter

This repository uses MegaLinter for comprehensive linting across multiple languages and file types.
We use this so that all additional assets in the repository (e.g. YAML files, Markdown files, etc.) are also linted and checked for formatting issues, without having to set up specific linters for each file type.

To run MegaLinter locally, you can use the following command:

```bash
docker run --platform linux/amd64 --rm \
    -v /var/run/docker.sock:/var/run/docker.sock:rw \
    -v $(pwd):/tmp/lint:rw \
    oxsecurity/megalinter:v8
```

#### Documentation linting and building

This repository uses Markdownlint for linting the documentation. To run Markdownlint locally, you can use the following:

1. Install the dependencies for Markdownlint.

   ```bash
   npm install -g markdownlint-cli
   ```

2. Run Markdownlint.

   ```bash
   markdownlint .
   ```

   _(Optional) Add the `--fix` flag to automatically fix any linting issues that can be fixed._

   ```bash
   markdownlint . --fix
   ```

To test that the documentation builds correctly, you can use the following command:

```bash
poetry run mkdocs build
```
