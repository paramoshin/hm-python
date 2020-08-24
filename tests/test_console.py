"""Test cases for console module."""


from unittest.mock import Mock

import pytest
import requests
from click.testing import CliRunner
from hm_python import console
from pytest_mock import MockerFixture


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interface."""
    return CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockerFixture) -> Mock:
    """Fixture for mocking random wikipedia page."""
    return mocker.patch("hm_python.wikipedia.random_page")


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It exits with a status code zero."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It prints wikipedia page title."""
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It invoke requests.get."""
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_ru_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It uses russian wikipedia by default."""
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "ru.wikipedia.org" in args[0]


def test_main_fails_on_request_error(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It exits with non-zero status code if the request fails."""
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It prints error message if request fails."""
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    """It exits with a status code of zero (end-to-end)."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0
