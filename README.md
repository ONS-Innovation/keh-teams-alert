# keh-teams-alert

Python module for sending a JSON payload (`channel` and `message`) to an HTTP webhook using an Entra ID (Azure AD) access token acquired via `azure-identity`.

## Table of Contents

- [keh-teams-alert](#keh-teams-alert)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Makefile](#makefile)
  - [Using the Package](#using-the-package)
    - [Azure Entra ID App Registration](#azure-entra-id-app-registration)
    - [End User Instructions](#end-user-instructions)
      - [Installation](#installation)
      - [Usage](#usage)
      - [Error Handling](#error-handling)
    - [Developer Instructions](#developer-instructions)
  - [Package Structure](#package-structure)
  - [Deployment](#deployment)
  - [Documentation](#documentation)
    - [GitHub Actions for Documentation](#github-actions-for-documentation)
    - [Local Development of Documentation](#local-development-of-documentation)
  - [Linting and Testing](#linting-and-testing)
    - [GitHub Actions](#github-actions)
    - [Running Tests and Linters Locally](#running-tests-and-linters-locally)
      - [Primary Language](#primary-language)
      - [MegaLinter](#megalinter)
      - [Documentation linting and building](#documentation-linting-and-building)

## Prerequisites

- Python 3.12 or higher
- Poetry for dependency management (>=2.x)
- Node.js and npm for documentation linting (Markdownlint)

## Makefile

This project uses a Makefile to simplify common tasks.
To see the available commands, run:

```bash
make help
```

## Using the Package

### Azure Entra ID App Registration

This package requires an Azure Entra ID (Azure AD) App Registration with client credentials (tenant id, client id, client secret).
This is required for the package to acquire an access token for the HTTP webhook, and send the JSON payload securely.

The tool digesting this repository is responsible for securely managing the Azure Entra ID (Azure AD) credentials and passing them to this library during use.

### End User Instructions

#### Installation

To use the package, you can install it using your preferred method (e.g. pip, Poetry, etc.) and then import the relevant modules and functions in your code.

```bash
# Using pip
pip install git+https://github.com/ONS-Innovation/keh-teams-alert@<version>

# or using Poetry
poetry add git+https://github.com/ONS-Innovation/keh-teams-alert@<version>
```

#### Usage

Then, in your Python code, you can import the relevant modules and functions:

```python
from keh_teams_alert import TeamsAlertClient

client = TeamsAlertClient(
    tenant_id="<tenant_id>",
    client_id="<client_id>",
    client_secret="<client_secret>",
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

#### Error Handling

Token acquisition errors (bad credentials/consent) and network errors are caught and re-raised as `RuntimeError` with context from the underlying Azure SDK exception.

### Developer Instructions

When developing the package, you can use the `tests/manual_testing.py` file for manual testing of the package during development.
This file has a `TeamsAlertClient` instance already setup which can be used to test the webhook integration.

To use the latest version of the package in the `manual_testing.py` file, you can install the package into your virtual environment:

```bash
pip install .
```

**Note:** This should be done from the root directory of the repository, and you should have your virtual environment activated.

Whenever you make changes to the package, you will need to reinstall it for the changes to be reflected in the `manual_testing.py` file.

## Package Structure

```text
src/
  └── keh_teams_alert/
      └── __init__.py     # File containing the main implementation of the keh_teams_alert package
```

## Deployment

The package can be deployed to GitHub Releases using the GitHub Actions workflow defined in `.github/workflows/publish-release.yml`.

This workflow is triggered on pushes to tags matching the pattern "v\*". The tag must follow the format "v0.0.0" (e.g. "v0.1.0", "v1.0.0", etc.) for the workflow to run successfully.

A production release will be created when a tag is pushed that follows the format "v0.0.0" (e.g. "v0.1.0", "v1.0.0", etc.). A pre-release will be created when a tag is pushed that follows the format "v0.0.0-rc" (e.g. "v0.1.0-rc", "v1.0.0-rc", etc.). This allows for both stable releases and pre-releases to be created and published to GitHub Releases.

Package versioning is derived dynamically from the git tag during the release workflow. To create a new release, create and push a version tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

This triggers the GitHub Actions workflow to build and publish the package to GitHub Releases using version `0.1.0` derived from tag `v0.1.0`.

**Note:** It is important that GitHub Releases are _only_ created via the GitHub Actions workflow, and not manually via the GitHub UI. This is because the workflow ensures that the package is built and published correctly.

## Documentation

This repository uses [MkDocs](https://www.mkdocs.org/) for documentation. The documentation source files are located in the `docs` directory.

### GitHub Actions for Documentation

MkDocs gets deployed to GitHub Pages using GitHub Actions. The workflow for this is located at `.github/workflows/deploy-docs.yml`.
Before deployment, another GitHub Action workflow runs to check that the documentation builds correctly and has no linting or formatting issues.
This workflow is located at `.github/workflows/ci-docs.yml`.

### Local Development of Documentation

To run the documentation locally:

1. Create a Python virtual environment and activate it.

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install the dependencies for MkDocs.

   ```bash
   make docs-install
   ```

3. Run the MkDocs development server.

   ```bash
   make docs-serve
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

#### Primary Language

To run the linters and formatters for the primary language (Python) locally, you can use the following command:

```bash
make lint
```

To apply automatic fixes for any linting or formatting issues found, you can use:

```bash
make fmt
```

To run the tests locally, you can use:

```bash
make test
```

#### MegaLinter

This repository uses MegaLinter for comprehensive linting across multiple languages and file types.
We use this so that all additional assets in the repository (e.g. YAML files, Markdown files, etc.) are also linted and checked for formatting issues, without having to set up specific linters for each file type.

To run MegaLinter locally, you can use the following command:

```bash
make megalinter
```

#### Documentation linting and building

This repository uses Markdownlint for linting the documentation. To run Markdownlint locally, you can use the following:

```bash
make docs-lint
```

**Note:** This will install `markdownlint-cli` globally via npm if it is not already installed.

To apply automatic fixes for any linting issues found by Markdownlint, you can use:

```bash
make docs-fix
```

To test that the documentation builds correctly, you can use the following command:

```bash
make docs-build
```

**Note:** This depends on MkDocs being set up for the repository. Instructions for setting up MkDocs can be found in the [Documentation](#documentation) section of this README.
