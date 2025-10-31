# Contributing guidelines

This document provides guidelines for contributing to the dataorc project.

## Requesting changes

[Create a new issue](https://github.com/equinor/dataorc/issues/new/choose).

## Making changes

1. Create a new branch. For external contributors, create a fork.
1. Make your changes.
1. Commit your changes.

    Follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for semantic commit messages.

1. Create a pull request to merge your changes into branch `main`.

## Add new package

Adding and publishing a new package requires some initial setup:

1. Change to the packages directory:

    ```console
    cd packages
    ```

1. Create a new project:

    ```console
    uv init --package <project-name>
    ```

    For example, create a new project `dataorc-example`:

    ```console
    uv init --package dataorc-example
    ```

1. Add the package to `release-please-config.json`.

1. Contact an administrator of the [Equinor user on PyPI](https://pypi.org/user/Equinor/) and request a ["pending" trusted publisher](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/#github-actions) to be registered with the following configuration:

    - **PyPI project name**: `<project-name>` (for example, `dataorc-core`)
    - **Owner**: `equinor`
    - **Repository name**: `dataorc`
    - **Workflow name**: `release.yml`
    - **Environment name**: `pypi`

Once the project files have been created and the trusted publisher has been registered, you can start adding features to your package!

## Contributing to Documentation

We use [MkDocs](https://www.mkdocs.org/) with the [Material theme](https://squidfunk.github.io/mkdocs-material/) for documentation. Changes are automatically deployed to <https://equinor.github.io/dataorc/> when merged to main.

### Quick Start

1. **Setup**:

   ```console
   uv venv
   .\.venv\Scripts\Activate.ps1  # Windows
   uv pip install -r docs/requirements.txt
   ```

2. **Preview locally**:

   ```console
   python -m mkdocs serve
   ```

   Documentation available at <http://127.0.0.1:8000/dataorc/>

3. **Test before PR**:

   ```console
   python -m mkdocs build --strict
   ```

### Adding Content

- Edit `.md` files in `docs/` directory
- Add new pages to `nav` section in `mkdocs.yml`
- Use standard Markdown syntax

**Note**: Always use `python -m mkdocs` (not just `mkdocs`) to avoid path issues.

