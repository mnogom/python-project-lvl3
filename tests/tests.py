"""Module to run tests."""

import pytest
import tempfile
import os

from page_loader.loader import get_local_name, download


URL_1_1 = "https://ru.hexlet.io/courses"
URL_1_2 = "http://ru.hexlet.io/courses"
URL_2 = "https://ru.hexlet.io/projects/51/members/14466?step=1"

PATH_1 = "/var/tmp"
PATH_2 = os.getcwd()

RESULT_1 = "ru-hexlet-io-courses.html"
RESULT_2 = "ru-hexlet-io-projects-51-members-14466?step-1.html"


@pytest.mark.parametrize("url, result",
                         [(URL_1_1, RESULT_1),
                          (URL_1_2, RESULT_1),
                          (URL_2, RESULT_2)])
def test_get_filename(url, result):
    assert get_local_name(url) == result


@pytest.mark.parametrize("url, result",
                         [(URL_1_1, RESULT_1),
                          (URL_2, RESULT_2)])
def test_download(url, result):
    with tempfile.TemporaryDirectory(dir="tests/fixtures") as temp_dir:
        assert download(url, temp_dir) == f"/{temp_dir}/{result}"
        assert os.path.isfile(f"{temp_dir}/{result}") is True
