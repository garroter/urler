import secrets
import string

from django.db import IntegrityError

from links.models import Link

_ALPHABET = string.ascii_letters + string.digits
MAX_ATTEMPTS = 10


def create_link(url: str, length: int = 7) -> Link:
    for _ in range(MAX_ATTEMPTS):
        code = "".join(secrets.choice(_ALPHABET) for _ in range(length))
        try:
            return Link.objects.create(code=code, url=url)
        except IntegrityError:
            continue
    raise RuntimeError(f"Could not generate a unique short code after {MAX_ATTEMPTS} attempts")
