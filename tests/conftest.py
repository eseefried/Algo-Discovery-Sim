import pytest

from a2m.sandbox import Sandbox
from a2m.tasks import load_card


@pytest.fixture(scope="session")
def sandbox():
    return Sandbox(profile="auto", timeout_s=120)


@pytest.fixture(scope="session")
def affine_card():
    return load_card("arxiv-1407.6402")


@pytest.fixture(scope="session")
def adder_card():
    return load_card("arxiv-1411.5949")
