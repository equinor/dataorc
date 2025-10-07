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

We use [MkDocs](https://www.mkdocs.org/) with the [Material theme](https://squidfunk.github.io/mkdocs-material/) to build our documentation. The documentation is automatically deployed to [Read the Docs](https://readthedocs.org/) when changes are pushed to the main branch.

### Building Documentation Locally

To preview documentation changes locally before submitting a pull request:

1. **Install documentation dependencies**:

   ```console
   pip install -r docs/requirements.txt
   ```

   This installs MkDocs, the Material theme, and related plugins.

2. **Build the documentation**:

   ```console
   mkdocs build
   ```

   This creates a static site in the `site/` directory.

3. **Serve the documentation locally**:

   ```console
   # If you're using a virtual environment, activate it first
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   source .venv/bin/activate     # Linux/macOS

   # Start the development server
   python -m mkdocs serve
   ```

   The documentation will be available at <http://127.0.0.1:8000/>

4. **Make changes and preview**:
   - Edit any `.md` files in the `docs/` directory
   - The browser will automatically refresh with your changes (live reload)
   - Add new pages by creating new `.md` files and updating the `nav` section in `mkdocs.yml`

### Documentation Structure

```text
docs/
├── index.md              # Homepage
├── version-matrix.md     # Version compatibility matrix
├── requirements.txt      # Documentation dependencies
└── ...                   # Additional documentation pages
mkdocs.yml               # MkDocs configuration file
```

### Writing Documentation

- Use standard Markdown syntax
- Follow the existing style and structure
- Include code examples where helpful
- Test all code examples to ensure they work
- Add new pages to the navigation in `mkdocs.yml`

### Troubleshooting Documentation Builds

If you encounter issues with the local documentation server:

1. **Python path issues**: Use `python -m mkdocs serve` instead of `mkdocs serve`
2. **Missing dependencies**: Reinstall with `pip install -r docs/requirements.txt`
3. **Version conflicts**: Check that your Python environment matches the requirements
4. **Virtual environment**: Ensure you're in the correct virtual environment

The local preview gives you the exact same experience as the deployed Read the Docs site!
