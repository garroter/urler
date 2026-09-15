from typing import Any

from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from links.models import Link
from links.serializers import LinkSerializer


class ShortenView(generics.CreateAPIView[Link]):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class RedirectView(generics.GenericAPIView[Link]):
    queryset = Link.objects.all()

    def get(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
        try:
            link = self.get_queryset().get(code=kwargs["code"])
        except Link.DoesNotExist:
            raise NotFound() from None
        return HttpResponseRedirect(link.url)
