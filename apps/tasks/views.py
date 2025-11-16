from typing import Any


from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def hello_view(
    request: HttpRequest,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any]
) -> HttpResponse:

    return render(
        request=request,
        template_name="index.html",
        context={"name": "Nuray", "names": []},
        status=200
    )