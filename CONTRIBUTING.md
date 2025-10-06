# Contributing guidelines

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
