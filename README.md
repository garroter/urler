# urler

API do skracania URL-i, oparte o Django + Django REST Framework.

## Wymagania

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Instalacja

```bash
uv sync
```

## Uruchomienie

```bash
uv run manage.py migrate
uv run manage.py runserver
```

## Testy

```bash
uv run pytest
```

## Typowanie i lint

```bash
uv run mypy .
uv run ruff check .
uv run ruff format .
```

## pre-commit

```bash
uv run pre-commit install
```

mypy i pytest są celowo poza pre-commitem (za wolne) — odpalać ręcznie lub w CI.
