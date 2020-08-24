import click
import requests

API_URL = "https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"


def random_page(lang="ru"):
    url = API_URL.format(lang=lang)

    try:
        with requests.get(url) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as e:
        message = str(e)
        raise click.ClickException(message)
