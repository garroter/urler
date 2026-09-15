import pytest
from rest_framework.test import APIClient

from links.models import Link


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
def test_shorten_creates_link_and_returns_expected_shape(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/shorten/", {"url": "https://example.com/very/long/path"}, format="json"
    )

    assert response.status_code == 201
    data = response.json()
    assert set(data.keys()) == {"code", "short_url", "url"}
    assert data["url"] == "https://example.com/very/long/path"
    assert data["short_url"].endswith(f"/{data['code']}/")
    assert Link.objects.filter(code=data["code"]).exists()


@pytest.mark.django_db
def test_shorten_with_invalid_url_returns_400(api_client: APIClient) -> None:
    response = api_client.post("/api/shorten/", {"url": "not-a-url"}, format="json")

    assert response.status_code == 400
    assert response.json() == {"url": ["Enter a valid URL."]}


@pytest.mark.django_db
def test_redirect_for_existing_code(api_client: APIClient) -> None:
    link = Link.objects.create(code="abc1234", url="https://example.com/target")

    response = api_client.get(f"/{link.code}/")

    assert response.status_code == 302
    assert response["Location"] == "https://example.com/target"


@pytest.mark.django_db
def test_redirect_for_missing_code_returns_404(api_client: APIClient) -> None:
    response = api_client.get("/doesnotexist/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found."}
