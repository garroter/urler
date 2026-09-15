from django.urls import URLPattern, path

from links.views import RedirectView, ShortenView

urlpatterns: list[URLPattern] = [
    path("api/shorten/", ShortenView.as_view(), name="shorten"),
    path("<str:code>/", RedirectView.as_view(), name="redirect"),
]
