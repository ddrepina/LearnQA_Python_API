import pytest


def test_len_phrase():
    phrase = input("Set a phrase")
    assert len(phrase) < 15, f"len(phrase) > 15"
