"""Client for wikipedia REST API v.1."""


from typing import Any

import click
import requests
from pydantic import BaseModel, ValidationError


class Page(BaseModel):
    """Page resource.

    Attributes:
        title: The title of a Wikipedia page.
        extract: Short page summary.
    """

    title: str
    extract: str


API_URL: str = "https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"


def random_page(lang: str = "ru") -> Page:
    """Return a random page.

    Performs a GET request to the /page/random/summary endpoint.

    Args:
        lang: Language of Wikipedia page. Defaults to russian wikipedia ("ru").

    Returns:
        A page resource.

    Raises:
        ClickException: The http-request failed or the http-response container an invalid body.

    Example:
        >>> from hm_python import wikipedia
        >>> page = wikipedia.random_page(lang="en")
        >>> bool(page.title)
        True
    """
    url = API_URL.format(lang=lang)

    try:
        with requests.get(url) as response:
            response.raise_for_status()
            return Page.parse_obj(response.json())
    except (requests.RequestException, ValidationError) as e:
        message = str(e)
        raise click.ClickException(message)
