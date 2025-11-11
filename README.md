# dataorc

[![CI](https://github.com/equinor/dataorc/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/equinor/dataorc/actions/workflows/ci.yml)

## Developing

We use [uv](https://docs.astral.sh/uv/) to have one synchronous development environment. See [installing uv](https://docs.astral.sh/uv/getting-started/installation/).

Once uv is installed, clone the repository:

```console
git clone https://github.com/equinor/dataorc.git && cd dataorc
```

Sync the development environment:

```console
uv sync --all-extras
```

### Building documentation

Build the documentation and run a local development server:

```console
uv run mkdocs serve --strict
```

The documentation will be served locally at <http://127.0.0.1:8000/dataorc/>.

## Contributing

See [contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the terms of the [MIT license](LICENSE).
