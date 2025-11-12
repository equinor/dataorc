# Contributing guidelines

This document provides guidelines for contributing to the dataorc project.

## Requesting changes

[Create a new issue](https://github.com/equinor/dataorc/issues/new/choose).

## Making changes

1. Create a new branch. For external contributors, create a fork.
1. Make your changes.
1. Commit your changes.
1. Create a pull request to merge your changes into branch `main`.

    Follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for semantic pull request titles, where scope is the package that you've made changes to, for example:

    - If you've added a feature in the `dataorc-utils` package:

        ```plaintext
        feat(utils): add core pipeline config tool `CorePipelineConfig`
        ```

    - If you've fixed a bug in the `dataorc-utils` package:

        ```plaintext
        fix(utils): `CorePipelineConfig` returns incorrect Data Lake path
        ```

    - If you've updated documentation for the `dataorc-utils` package:

        ```plaintext
        docs(utils): clarify parameters in `CorePipelineConfig` usage example
        ```

    - If you've added a feature in the main `dataorc` package:

        ```plaintext
        feat: install package `dataorc-utils`
        ```

## Add new package

Adding and publishing a new package requires some initial setup:

1. Change to the scripts directory:

    ```console
    cd scripts
    ```

1. Run the `bootstrap-package.sh` script to bootstrap a new package:

    ```console
    ./bootstrap-package.sh <project-name>
    ```

    For example, to bootstrap a new package `dataorc-core`, run the script with the following arguments:

    ```console
    ./bootstrap-package.sh dataorc-core
    ```

    The project name must contain only lowercase letters and dashes (`-`).

    A new directory `packages/<project-name>` containing the required project files will be created.

1. Contact an administrator of the [Equinor user on PyPI](https://pypi.org/user/Equinor/) and request a ["pending" trusted publisher](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/#github-actions) to be registered with the following configuration:

    - **PyPI project name**: `<project-name>` (for example, `dataorc-core`)
    - **Owner**: `equinor`
    - **Repository name**: `dataorc`
    - **Workflow name**: `release.yml`
    - **Environment name**: `pypi`

Once the project files have been created and the trusted publisher has been registered, you can start adding features to your package!

## Contributing to Documentation

We use [MkDocs](https://www.mkdocs.org/) with the [Material theme](https://squidfunk.github.io/mkdocs-material/) for documentation. Changes are automatically deployed to <https://equinor.github.io/dataorc/> when merged to main.

### Adding Content

- Edit `.md` files in `docs/` directory
- Add new pages to `nav` section in `mkdocs.yml`
- Use standard Markdown syntax
