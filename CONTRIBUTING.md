# Contributing guidelines

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
