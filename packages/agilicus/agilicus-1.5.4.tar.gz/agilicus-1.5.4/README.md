## Agilicus SDK (Python)

The overall API is [documented](https://www.agilicus.com/api).

A subset of this code (that which accesses the above API)
is [generated](agilicus/agilicus_api_README.md)

## Build

(first generate the api access, 'cd ..; ./local-build')

```
poetry install
poetry run pytest
```

To run the CLI from the development venv:
gene

`poetry run python -m agilicus.main`

To format & lint:

```
poetry run black .
poetry run flake8
```

## CLI Usage

Credentials are cached in ~/.config/agilicus, per issuer.

```
agilicus-cli --client_id admin-portal --issuer https://auth.cloud.egov.city list-applications
```
