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

## API

```
POST /api/shorten/  {"url": "..."} -> 201 {"code", "short_url", "url"}
GET  /<code>/       -> 302 redirect (Location: oryginalny url) / 404
```

404 zwraca `{"detail": "Not found."}` (jawnie, zamiast domyślnego
`get_object_or_404`) - tak żeby treść błędu była spójna z resztą API, a nie
zawierała nazwy modelu Django w komunikacie.

`url` jest walidowany jako poprawny URL przez DRF (`URLField` na podstawie
pola modelu) — brak/zły format -> `400` z listą błędów per pole.

### Ręczne testowanie (curl)

```bash
curl -X POST http://localhost:8000/api/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://szkolawchmurze.org/"}'
# -> {"code": "...", "short_url": "http://localhost:8000/<code>/", "url": "..."}

curl -i http://localhost:8000/<code>/
# -> 302, Location: https://szkolawchmurze.org/

curl -X POST http://localhost:8000/api/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"url": "not-a-url"}'
# -> 400 {"url": ["Enter a valid URL."]}
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
