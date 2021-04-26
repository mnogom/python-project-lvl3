"""Some special components tests."""

import pytest

from page_loader.loader import get_local_name


INPUT = ("https://ru.hexlet.io/",
         "https://ru.hexlet.io",
         "http://ru.hexlet.io",
         "https://ru.hexlet.io/courses",
         "https://ru.hexlet.io/courses/intro_to_git/",
         "https://ru.hexlet.io/my/ratings/month?q%5Bcity_id_eq%5D=1")

RESULT = ("ru-hexlet-io.html",
          "ru-hexlet-io.html",
          "ru-hexlet-io.html",
          "ru-hexlet-io-courses.html",
          "ru-hexlet-io-courses-intro_to_git.html",
          "ru-hexlet-io-my-ratings-month?q-5Bcity_id_eq-5D=1.html")


@pytest.mark.parametrize("url, result",
                         [
                             (a, b) for a, b in zip(INPUT, RESULT)
                         ])
def test_local_name(url, result):
    assert get_local_name(url, ".html") == result
