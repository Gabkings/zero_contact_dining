import pytest

from .factories import (
    UserFactory,
    AdminFactory,
)


@pytest.fixture
def customer():

    return UserFactory()


@pytest.fixture
def admin():

    return AdminFactory()