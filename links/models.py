from django.db import models


class Link(models.Model):
    code = models.CharField(max_length=10, unique=True)
    url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.code
