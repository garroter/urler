import string
from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest
from django.db import IntegrityError

from links.models import Link
from links.services import MAX_ATTEMPTS, create_link

_CODE_ALPHABET = set(string.ascii_letters + string.digits)


@pytest.fixture
def mock_link_create() -> Iterator[MagicMock]:
    with patch("links.services.Link.objects.create") as mock:
        mock.return_value = MagicMock(spec=Link)
        yield mock


def test_create_link_saves_generated_code_and_url(mock_link_create: MagicMock) -> None:
    create_link("https://example.com")

    assert mock_link_create.call_count == 1
    _, kwargs = mock_link_create.call_args
    assert kwargs["url"] == "https://example.com"
    code = kwargs["code"]
    assert len(code) == 7
    assert set(code) <= _CODE_ALPHABET


def test_create_link_respects_custom_length(mock_link_create: MagicMock) -> None:
    create_link("https://example.com", length=9)

    _, kwargs = mock_link_create.call_args
    assert len(kwargs["code"]) == 9


def test_create_link_retries_on_code_collision(mock_link_create: MagicMock) -> None:
    link = MagicMock(spec=Link)
    mock_link_create.side_effect = [IntegrityError, link]

    result = create_link("https://example.com")

    assert result is link
    assert mock_link_create.call_count == 2


def test_create_link_raises_after_exhausting_attempts(mock_link_create: MagicMock) -> None:
    mock_link_create.side_effect = IntegrityError

    with pytest.raises(RuntimeError):
        create_link("https://example.com")

    assert mock_link_create.call_count == MAX_ATTEMPTS
