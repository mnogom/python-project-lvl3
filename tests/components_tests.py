"""Some special components tests."""

import pytest
from logging import DEBUG, WARNING

from page_loader.loader import _generate_name
from page_loader.logger_agent import get_logger


INPUT = ("https://ru.hexlet.io/",
         "https://ru.hexlet.io/courses/intro_to_git/",
         "https://ru.hexlet.io/my/ratings/month?q%5Bcity_id_eq%5D=1")

RESULT = ("ru-hexlet-io.html",
          "ru-hexlet-io-courses-intro_to_git.html",
          "ru-hexlet-io-my-ratings-month-q-5Bcity_id_eq-5D-1.html")


@pytest.mark.parametrize("url, result",
                         [
                             (a, b) for a, b in zip(INPUT, RESULT)
                         ])
def test_local_name(url, result):
    assert _generate_name(url) == result


@pytest.mark.parametrize("debug_mode, right_log_level",
                         [(True, DEBUG),
                          (False, WARNING)])
def test_debug_activate(debug_mode, right_log_level):
    assert get_logger(debug_mode).level == right_log_level
