import pytest

from app import schemas


def test_package_with_nothing():
    with pytest.raises(ValueError):
        schemas.Package()


def test_package_with_ecosystem_only():
    with pytest.raises(ValueError):
        schemas.Package(ecosystem="dummy")


def test_query_with_nothing():
    with pytest.raises(ValueError):
        schemas.Query()


def test_query_with_version_without_package():
    with pytest.raises(ValueError):
        schemas.Query(version="dummy")