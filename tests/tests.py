"""Module to run tests."""

import pytest
from page_loader.core import hello_world


@pytest.mark.parametrize("a, b, c",
                         [(1, 2, 3),
                          (3, 10, 13)])
def test_sum(a, b, c):
    assert a + b == c


def test_core():
    assert hello_world() == "Hello, World!"
