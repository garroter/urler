from typing import Any

from rest_framework import serializers
from rest_framework.request import Request

from links.models import Link
from links.services import create_link


class LinkSerializer(serializers.ModelSerializer[Link]):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ["code", "short_url", "url"]
        read_only_fields = ["code"]

    def get_short_url(self, obj: Link) -> str:
        request: Request = self.context["request"]
        return request.build_absolute_uri(f"/{obj.code}/")

    def create(self, validated_data: dict[str, Any]) -> Link:
        return create_link(validated_data["url"])
