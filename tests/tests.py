"""Module to run tests."""

import pytest
import tempfile
import os

from page_loader.loader import download


URL_1 = "https://ru.hexlet.io/courses"
URL_2 = "https://ru.hexlet.io/projects/51/members/14466?step=1&item=2"

PATH_1 = "/var/tmp"
PATH_2 = os.getcwd()

RESULT_1 = "ru-hexlet-io-courses.html"
RESULT_2 = "ru-hexlet-io-projects-51-members-14466?step=1&item=2.html"


@pytest.mark.parametrize("url, result",
                         [(URL_1, RESULT_1),
                          (URL_2, RESULT_2)])
def test_download(url, result):
    with tempfile.TemporaryDirectory(dir="tests/fixtures/") as temp_dir:
        assert download(url, f"{temp_dir}/") == f"{temp_dir}/{result}"
        assert os.path.isfile(f"{temp_dir}/{result}") is True
        assert os.path.isdir(f"{temp_dir}/{result.replace('.html', '_files')}")
