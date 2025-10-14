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

