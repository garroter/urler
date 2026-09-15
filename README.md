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

## Model danych

`Link` (`links/models.py`): `code` (unikalny, indeksowany przez
`unique=True` - służy zarówno do wymuszenia unikalności jak i do szybszego pobierania według kodu
`GET /<code>/`), `url` oryginalny url z którego tworzymy skróconą wersję linku

Zapis kodu musi łapać `IntegrityError` i ponawiać próbę przy kolizji - celowo
sam pre-check w Pythonie nie chroni przed wyścigiem przy równoległych
requestach.

Brak wygasania linków - rekordy zostają w bazie na zawsze (celowo, poza
zakresem tego API).

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
