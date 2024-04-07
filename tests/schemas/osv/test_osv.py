import pytest

from mihama import schemas


def test_package_with_nothing():
    with pytest.raises(ValueError):  # noqa: PT011
        schemas.Package()  # type: ignore


def test_package_with_ecosystem_only():
    with pytest.raises(ValueError):  # noqa: PT011
        schemas.Package(ecosystem="dummy")  # type: ignore


def test_query_with_nothing():
    with pytest.raises(ValueError):  # noqa: PT011
        schemas.Query()


def test_query_with_version_without_package():
    with pytest.raises(ValueError):  # noqa: PT011
        schemas.Query(version="dummy")


def test_vulnerability(vulns: list[schemas.Vulnerability]):
    for v in vulns:
        schemas.Vulnerability.model_validate(v)
